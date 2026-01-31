# Tutor Engine Integration Guide

## Overview

The `tutor_engine.py` provides core functions for adaptive tutoring with misconception tagging heuristics. This document explains how it integrates with the `/tutor` route.

## Functions in `services/tutor_engine.py`

### 1. `load_topics()`
- **Purpose**: Loads algebra topics data from `data/algebra_topics.json`
- **Returns**: `bool` (True if successful)
- **Called**: Automatically in `__init__`, can be called manually to reload
- **Usage**: `tutor_engine.load_topics()`

### 2. `choose_difficulty(student_profile, state)`
- **Purpose**: Determines appropriate difficulty level based on student performance
- **Parameters**:
  - `student_profile`: Dict with `confidence`, `grade_year`, etc.
  - `state`: Dict with `weakAreas`, `mastered`, `difficulty`
- **Returns**: `'foundation'`, `'core'`, or `'higher'`
- **Logic**:
  - Moves down if `weakAreas > 3`
  - Moves up if `mastered > 2` and `weakAreas <= 1`
  - Uses confidence if no state history
  - Otherwise maintains current difficulty

### 3. `get_diagnostic_question(topic, difficulty)`
- **Purpose**: Gets diagnostic question for a topic at specified difficulty
- **Parameters**:
  - `topic`: Topic ID (e.g., `'linear_equations'`)
  - `difficulty`: `'foundation'`, `'core'`, or `'higher'`
- **Returns**: Dict with `question`, `answerType`, `correctAnswer`, `difficulty`, `id`

### 4. `update_state_from_student_answer(topic, student_answer, expected_signals)`
- **Purpose**: Evaluates student answer and tags misconceptions using heuristics
- **Parameters**:
  - `topic`: Topic ID
  - `student_answer`: Student's answer text
  - `expected_signals`: Dict with `correctAnswer`, `question`, `difficulty`
- **Returns**: Dict with `isCorrect` (bool) and `misconceptions` (list of labels)

## State Structure

The learning state stored in Flask session now includes:

```python
{
    'currentTopic': 'linear_equations',  # Topic ID
    'difficulty': 'core',                # foundation|core|higher
    'weakAreas': [],                     # List of misconception labels
    'mastered': [],                      # List of mastered concepts
    'stage': 'diagnostic',               # diagnostic|teach|explain_back|practice|mark|quiz|plan
    'lastQuestionId': None,             # ID of last question asked
    'nextFocus': '...'                   # What to focus on next
}
```

## Misconception Tagging Heuristics

### Inequalities (`solving_inequalities`)
- **`sign_flip_with_negatives`**: Detected when question has negative coefficient and inequality sign direction is wrong
- **`inequality_direction_errors`**: Detected when inequality direction (`<` vs `>`) is incorrect

### Expanding Brackets (`expanding_brackets`)
- **`distribution_incomplete`**: Detected when answer has fewer terms than expected (only first term multiplied)

### Factorisation (`factorisation`)
- **`missing_common_factors`**: Detected when question has numbers but answer doesn't show common factor extraction
- **`wrong_factor_pairs`**: Detected when quadratic question but answer doesn't have 2 factors

### Simultaneous Equations (`simultaneous_equations`)
- **`elimination_sign_mistakes`**: Detected when answer format is wrong (missing comma)
- **`no_substitution_back`**: Detected when only one variable provided instead of two

### Linear Equations (`linear_equations`)
- **`inverse_operations_confusion`**: Detected when signs are consistently wrong compared to question
- **`sign_errors`**: Detected when answer has opposite sign but same magnitude

**Fallback**: If no specific misconception detected, tags `arithmetic_errors`

## Integration with `/tutor` Route

### Flow:

1. **Initial Setup** (`/student-setup`):
   ```python
   # Choose initial difficulty
   initial_difficulty = tutor_engine.choose_difficulty(student_profile, empty_state)
   
   # Initialize state with stage and lastQuestionId
   session['learning_state'] = {
       'stage': 'diagnostic',
       'lastQuestionId': None,
       ...
   }
   ```

2. **Reset Mode** (`/tutor` with `mode='reset'`):
   ```python
   # Choose difficulty
   difficulty = tutor_engine.choose_difficulty(student_profile, state)
   
   # Get diagnostic question
   diagnostic = tutor_engine.get_diagnostic_question(topic, difficulty)
   
   # Store question ID
   learning_state['lastQuestionId'] = diagnostic['id']
   ```

3. **Answer Evaluation** (when student responds):
   ```python
   # Evaluate answer and tag misconceptions
   evaluation = tutor_engine.update_state_from_student_answer(
       topic=topic,
       student_answer=student_message,
       expected_signals={
           'correctAnswer': diagnostic['correctAnswer'],
           'question': diagnostic['question'],
           'difficulty': difficulty
       }
   )
   
   # Update weak areas
   if evaluation['misconceptions']:
       learning_state['weakAreas'].extend(evaluation['misconceptions'])
   
   # Update mastered
   if evaluation['isCorrect']:
       learning_state['mastered'].append(f"{topic}_{difficulty}")
   
   # Adjust difficulty
   new_difficulty = tutor_engine.choose_difficulty(student_profile, learning_state)
   learning_state['difficulty'] = new_difficulty
   
   # Update stage
   if learning_state['stage'] == 'diagnostic' and evaluation['isCorrect']:
       learning_state['stage'] = 'teach'
   ```

4. **Gemini Response Handling**:
   - Gemini response includes `stateUpdate` in JSON
   - Route merges Gemini's state update with current state
   - Preserves `stage` and `lastQuestionId` if not in Gemini response

## Key Integration Points

### In `app.py`:

1. **Line ~60**: Initial state setup with `choose_difficulty()`
2. **Line ~195**: Reset mode uses `choose_difficulty()` and `get_diagnostic_question()`
3. **Line ~260-300**: Answer evaluation uses `update_state_from_student_answer()`
4. **Line ~310**: State preservation when merging Gemini response

## Example Usage

```python
# Initialize
tutor_engine = TutorEngine()

# Load topics (auto-called in __init__)
tutor_engine.load_topics()

# Choose difficulty
difficulty = tutor_engine.choose_difficulty(
    student_profile={'confidence': 3, 'grade_year': 'Year 10'},
    state={'weakAreas': ['sign_errors'], 'mastered': [], 'difficulty': 'core'}
)
# Returns: 'core' or 'foundation' or 'higher'

# Get diagnostic question
question = tutor_engine.get_diagnostic_question('linear_equations', 'core')
# Returns: {'question': '...', 'correctAnswer': '...', ...}

# Evaluate answer
result = tutor_engine.update_state_from_student_answer(
    topic='linear_equations',
    student_answer='x = 5',
    expected_signals={
        'correctAnswer': 'x = 4',
        'question': 'Solve: 2x + 3 = 11',
        'difficulty': 'core'
    }
)
# Returns: {'isCorrect': False, 'misconceptions': ['sign_errors', ...]}
```

## Notes

- Heuristics are **simple and reliable** for hackathon MVP
- They focus on **pattern matching** rather than full parsing
- **False positives** are acceptable (better to tag than miss)
- Heuristics can be enhanced later with more sophisticated NLP
- All functions are **stateless** (except `topic_data` which is loaded once)

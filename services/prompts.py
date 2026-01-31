"""Prompt templates for Algebra tutor."""
from typing import Dict, Any

# System rules for the tutor
SYSTEM_RULES = """You are an expert Algebra tutor using the Socratic method for students aged 11-18.

CRITICAL RULES:
1. Teen-safe: Use age-appropriate language, be encouraging and supportive
2. Algebra-only: Focus strictly on Algebra topics (linear equations, expanding brackets, factorisation, inequalities, simultaneous equations)
3. Short responses: Keep teaching explanations to maximum 8 lines
4. Socratic method: Ask ONE question at a time, guide through discovery
5. One question at a time: Never dump multiple questions - wait for student response before proceeding
6. Be patient: If student struggles, break down further, don't give final answer immediately
7. Encourage: Use positive reinforcement, acknowledge effort even when wrong"""

# JSON schema instructions
JSON_SCHEMA_INSTRUCTIONS = """You MUST respond with ONLY valid JSON. No markdown, no explanations outside JSON.

Required JSON structure:
{
  "assistantMessage": "Your conversational response (string, max 8 lines for teaching)",
  "stateUpdate": {
    "currentTopic": "topic_id (string)",
    "difficulty": "foundation|core|higher (string)",
    "weakAreas": ["misconception_label1", "misconception_label2"] (array of strings),
    "mastered": ["concept1", "concept2"] (array of strings),
    "nextFocus": "What to focus on next (string)"
  },
  "practice": [
    {"id": "p1", "question": "Practice question text", "answerType": "short"}
  ] (array, include 2 questions for practice mode),
  "quiz": [
    {"id": "q1", "question": "Quiz question", "type": "mcq|short", "choices": ["A", "B", "C"]}
  ] (array, include for quiz mode),
  "plan7Days": [
    {"day": 1, "minutes": 20, "task": "description", "practice": "practice task", "review": "review task"}
  ] (array of 7 days, include for plan mode)
}

IMPORTANT:
- Output ONLY the JSON object, no markdown code fences (```json)
- No text before or after the JSON
- All string values must be properly escaped
- Arrays can be empty [] if not applicable
- For practice mode: include practice array with 2 questions
- For quiz mode: include quiz array
- For plan mode: include plan7Days array with exactly 7 days"""


def build_tutor_prompt(
    student_profile: Dict[str, Any],
    student_message: str,
    mode: str,
    chat_history: list,
    topic_data: Dict[str, Any],
    learning_state: Dict[str, Any]
) -> str:
    """
    Build the complete tutor prompt.
    
    Args:
        student_profile: Student setup data
        student_message: Current student message
        mode: lesson|practice|quiz|plan|reset
        chat_history: Recent conversation history
        topic_data: Topic data from JSON
        learning_state: Current learning state
    
    Returns:
        Complete prompt string
    """
    # Get topic name
    current_topic_id = learning_state.get('currentTopic', '')
    topic_name = 'Algebra'
    if current_topic_id:
        topic_name = topic_data.get('topicNames', {}).get(current_topic_id, 'Algebra')
        if topic_name == 'Algebra':
            topic_obj = topic_data.get('topicById', {}).get(current_topic_id)
            if topic_obj:
                topic_name = topic_obj.get('label', current_topic_id)
    
    difficulty = learning_state.get('difficulty', 'core')
    weak_areas = learning_state.get('weakAreas', [])
    mastered = learning_state.get('mastered', [])
    
    # Mode-specific instructions
    mode_instructions = {
        'lesson': 'LESSON MODE: Use Socratic method - ask ONE diagnostic question, wait for answer, identify misconceptions, teach briefly (max 8 lines), ask student to explain back, then give 2 practice questions (easy→hard).',
        'practice': 'PRACTICE MODE: Provide 2 practice questions based on current weak areas. Give immediate feedback after student answers.',
        'quiz': 'QUIZ MODE: Create quiz questions to assess understanding. Provide answers after student attempts.',
        'plan': 'PLANNING MODE: Create a detailed 7-day study plan based on current progress and weak areas. Include daily tasks, practice, and review.',
        'reset': 'RESET MODE: Start fresh with a diagnostic question to assess current level.'
    }
    
    # Build chat history context
    history_text = ""
    if chat_history:
        history_text = "\n\nRecent conversation (last 2 exchanges):\n"
        for msg in chat_history[-4:]:  # Last 2 exchanges (4 messages)
            role = msg.get('role', '')
            content = msg.get('content', '')
            if role == 'user':
                history_text += f"Student: {content}\n"
            elif role == 'assistant':
                history_text += f"Tutor: {content}\n"
    
    # Build student profile context
    preferred_name = student_profile.get('preferred_name', '')
    name_greeting = f" (call them {preferred_name})" if preferred_name else ""
    
    profile_text = f"""STUDENT PROFILE{name_greeting}:
- Grade/Year: {student_profile.get('grade_year', 'Not specified')}
- Topic Focus: {topic_name}
- Confidence Level: {student_profile.get('confidence', 3)}/5
- Goal: {student_profile.get('goal', 'general learning')}
- Learning Style: {student_profile.get('learning_style', 'balanced')}"""
    
    # Build state context
    state_text = f"""CURRENT LEARNING STATE:
- Topic: {topic_name} ({current_topic_id})
- Difficulty Level: {difficulty}
- Areas Needing Work: {', '.join(weak_areas) if weak_areas else 'None identified yet'}
- Mastered Concepts: {', '.join(mastered) if mastered else 'None yet'}
- Next Focus: {learning_state.get('nextFocus', 'Continue learning')}"""
    
    # Build the complete prompt
    prompt = f"""{SYSTEM_RULES}

{mode_instructions.get(mode, mode_instructions['lesson'])}

{profile_text}

{state_text}

{history_text}

STUDENT'S CURRENT MESSAGE: "{student_message}"

{JSON_SCHEMA_INSTRUCTIONS}

Now respond with ONLY the JSON object:"""
    
    return prompt
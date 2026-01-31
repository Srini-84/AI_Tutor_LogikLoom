# LogikLoom - Adaptive Algebra Tutor

An intelligent Algebra tutoring system using Socratic method, adaptive difficulty, and misconception tracking. Built for hackathon with Flask and Google Gemini AI.

## Features

- **Socratic Tutoring Loop**: One question at a time, guided learning
- **Adaptive Difficulty**: Automatically adjusts (foundation → core → higher)
- **Misconception Tracking**: Identifies and addresses specific learning gaps
- **5 Algebra Topics**: Linear equations, Expanding brackets, Factorisation, Solving inequalities, Simultaneous equations
- **Multiple Modes**: Lesson, Practice, Quiz, 7-Day Plan, Reset
- **Privacy-Focused**: No sensitive personal information required

## Tech Stack

- **Backend**: Python 3.13, Flask 3.0.0
- **AI**: Google Gemini 2.0 Flash
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data**: JSON files (no database required)

## Setup Instructions

### 1. Prerequisites

- Python 3.13+
- Virtual environment (recommended)

### 2. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install packages
pip install -r requirements.txt
```

### 3. Set Environment Variable

**IMPORTANT**: You need a Google Gemini API key.

1. Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Set it as an environment variable:

```bash
# macOS/Linux
export GEMINI_API_KEY='your-api-key-here'

# Windows (PowerShell)
$env:GEMINI_API_KEY='your-api-key-here'

# Windows (CMD)
set GEMINI_API_KEY=your-api-key-here
```

**OR** create a `.env` file (not recommended for production):
```bash
GEMINI_API_KEY=your-api-key-here
```

### 4. Run the Application

```bash
python app.py
```

The app will start on `http://localhost:5000`

## Project Structure

```
LogikLoom/
├── app.py                 # Main Flask application
├── services/              # Tutor engine services
│   ├── __init__.py
│   ├── tutor_engine.py    # Adaptive tutoring logic
│   └── gemini_client.py   # Gemini API client
├── data/
│   └── algebra_topics.json  # Topics, diagnostics, misconceptions
├── templates/
│   └── index.html         # Frontend UI
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## API Endpoints

### `POST /student-setup`
Complete student setup wizard. Stores profile in session.

**Required fields:**
- `grade_year`: Year 7-13
- `topic`: One of the 5 algebra topics
- `confidence`: 1-5
- `goal`: exam_prep, homework, catch_up, learn_ahead
- `learning_style`: examples_first, practice_first, explain_slow, go_fast

**Optional fields:**
- `preferred_name`: String

### `POST /tutor`
Adaptive tutor endpoint with structured responses.

**Request:**
```json
{
  "studentMessage": "Student's answer or question",
  "mode": "lesson|practice|quiz|plan|reset"
}
```

**Response:**
```json
{
  "assistantMessage": "Tutor's response",
  "stateUpdate": {
    "currentTopic": "linear_equations",
    "difficulty": "foundation|core|higher",
    "weakAreas": ["sign_errors", "arithmetic_errors"],
    "mastered": ["linear_equations_foundation"],
    "nextFocus": "Focus on: Sign errors"
  },
  "practice": [
    {"id": "p1", "question": "...", "answerType": "short"}
  ],
  "quiz": [
    {"id": "q1", "question": "...", "type": "mcq|short", "choices": [...]}
  ],
  "plan7Days": [
    {"day": 1, "minutes": 20, "task": "...", "practice": "...", "review": "..."}
  ]
}
```

### `GET /health`
Health check endpoint.

## How It Works

1. **Student Setup**: 5-step wizard collects learning preferences (no sensitive info)
2. **Diagnostic Question**: System starts with a diagnostic based on confidence level
3. **Socratic Loop**: 
   - Ask one question
   - Evaluate answer
   - Identify misconceptions
   - Teach briefly (max 8 lines)
   - Ask student to explain back
   - Provide practice questions
4. **Adaptive Learning**: Difficulty and focus adjust based on performance
5. **State Tracking**: Weak areas and mastered concepts tracked in real-time

## Development Notes

- **No Database**: Uses Flask sessions for temporary storage
- **JSON Data**: Algebra topics stored in `data/algebra_topics.json`
- **Structured Responses**: Gemini outputs must be valid JSON (with fallback handling)
- **Privacy**: No name, age, school, or contact info required

## Troubleshooting

### API Key Issues
- Ensure `GEMINI_API_KEY` is set in environment
- Check API key is valid at [Google AI Studio](https://aistudio.google.com/apikey)
- Free tier available, no credit card required

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version: `python3 --version` (should be 3.13+)

### Tutor Not Responding
- Check browser console for errors
- Verify Flask server is running
- Check `/health` endpoint returns `tutor_engine_ready: true`

## License

Built for hackathon. Use as needed.

## Credits

- Google Gemini AI for intelligent tutoring
- Flask for lightweight backend
- Inter font for modern typography

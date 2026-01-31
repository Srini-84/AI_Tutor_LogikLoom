"""LogikLoom - Adaptive Algebra Tutor with Socratic Method."""
from flask import Flask, render_template, request, jsonify, session
import json
import os
import re

# Import services
from services.gemini_client import GeminiClient
from services.prompts import build_tutor_prompt
from services.tutor_engine import TutorEngine

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Enable CORS for Next.js frontend (optional - install flask-cors if needed)
try:
    from flask_cors import CORS
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
except ImportError:
    # CORS not installed, add manual headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

# Initialize services with API key from environment
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in environment. Set it before running tutor features.")

# Initialize Gemini client
try:
    gemini_client = GeminiClient(api_key=api_key) if api_key else None
except ValueError:
    gemini_client = None
    print("WARNING: Could not initialize Gemini client. Tutor features will not work.")

# Initialize tutor engine for diagnostic questions
tutor_engine = TutorEngine(api_key=api_key) if api_key else None


# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Route to handle Student Setup (formerly KYC)
@app.route('/student-setup', methods=['POST'])
def student_setup():
    """Handle student setup data - no sensitive personal info."""
    try:
        data = request.get_json()
        
        # Build student profile with required and optional fields
        student_profile = {
            # Required fields
            'grade_year': data.get('grade_year', ''),
            'topic': data.get('topic', ''),
            'confidence': int(data.get('confidence', 3)),
            'goal': data.get('goal', ''),
            'learning_style': data.get('learning_style', ''),
            # Optional fields
            'preferred_name': data.get('preferred_name', ''),
            'subject': data.get('subject', 'mathematics')  # Default to mathematics for now
        }
        
        # Validate required fields
        required = ['grade_year', 'topic', 'confidence', 'goal', 'learning_style']
        missing = [field for field in required if not student_profile.get(field)]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400
        
        # Store in session
        session['student_profile'] = student_profile
        
        # Choose initial difficulty using tutor engine if available
        initial_difficulty = 'foundation' if student_profile['confidence'] <= 2 else 'core'
        if tutor_engine:
            initial_difficulty = tutor_engine.choose_difficulty(
                student_profile,
                {'weakAreas': [], 'mastered': [], 'difficulty': initial_difficulty}
            )
        
        # Initialize learning state with new structure
        session['learning_state'] = {
            'currentTopic': student_profile['topic'],
            'difficulty': initial_difficulty,
            'weakAreas': [],
            'mastered': [],
            'stage': 'diagnostic',
            'lastQuestionId': None,
            'nextFocus': f"Starting with {student_profile['topic']}"
        }
        
        # Initialize chat history
        session['chat_history'] = []
        
                return jsonify({
            'success': True,
            'message': 'Student setup completed successfully',
            'student_profile': student_profile
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def parse_json_robust(text: str) -> dict:
    """
    Robustly parse JSON from text, handling code fences and extra text.
    
    Args:
        text: Text that may contain JSON
    
    Returns:
        Parsed JSON dict, or None if parsing fails
    """
    if not text:
        return None
    
    text = text.strip()
    
    # Remove markdown code fences
    if '```json' in text:
        json_start = text.find('```json') + 7
        json_end = text.find('```', json_start)
        if json_end != -1:
            text = text[json_start:json_end].strip()
    elif '```' in text:
        json_start = text.find('```') + 3
        json_end = text.find('```', json_start)
        if json_end != -1:
            text = text[json_start:json_end].strip()
    
    # Find first '{' and last '}'
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        text = text[first_brace:last_brace + 1]
    
    # Try to parse JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to fix common issues
        # Remove trailing commas before closing braces/brackets
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None


def create_safe_fallback_response(learning_state: dict, student_message: str = "") -> dict:
    """
    Create a safe fallback JSON response when parsing fails.
    
    Args:
        learning_state: Current learning state
        student_message: Student's message (if any)
    
    Returns:
        Safe fallback response dict
    """
    return {
        'assistantMessage': "I'm having trouble understanding that. Could you try rephrasing your answer or question? Let's continue learning!",
        'stateUpdate': learning_state,
        'practice': [],
        'quiz': [],
        'plan7Days': []
    }


# Route for adaptive Algebra tutor
@app.route('/tutor', methods=['POST'])
def tutor():
    """Adaptive Algebra tutor with Socratic method and structured responses."""
    if not gemini_client:
        return jsonify({
            'error': 'Gemini client not initialized. Please set GEMINI_API_KEY environment variable.'
        }), 500
    
    try:
        data = request.get_json()
        student_message = data.get('studentMessage', '')
        mode = data.get('mode', 'lesson')  # lesson, practice, quiz, plan, reset
        
        if not student_message and mode != 'reset':
            return jsonify({'error': 'No student message provided'}), 400
        
        # Get student profile and state from session
        student_profile = session.get('student_profile', {})
        if not student_profile:
            return jsonify({
                'error': 'Student profile not found. Please complete student setup first.'
            }), 400
        
        learning_state = session.get('learning_state', {
            'currentTopic': student_profile.get('topic', 'linear_equations'),
            'difficulty': 'core',
            'weakAreas': [],
            'mastered': [],
            'stage': 'diagnostic',
            'lastQuestionId': None,
            'nextFocus': 'Starting learning'
        })
        
        chat_history = session.get('chat_history', [])
        
        # Handle reset mode
        if mode == 'reset':
            # Choose initial difficulty
            initial_difficulty = 'foundation' if student_profile.get('confidence', 3) <= 2 else 'core'
            if tutor_engine:
                initial_difficulty = tutor_engine.choose_difficulty(
                    student_profile,
                    {'weakAreas': [], 'mastered': [], 'difficulty': initial_difficulty}
                )
            
            session['learning_state'] = {
                'currentTopic': student_profile.get('topic', 'linear_equations'),
                'difficulty': initial_difficulty,
                'weakAreas': [],
                'mastered': [],
                'stage': 'diagnostic',
                'lastQuestionId': None,
                'nextFocus': f"Starting fresh with {student_profile.get('topic', 'Algebra')}"
            }
            session['chat_history'] = []
            learning_state = session['learning_state']
            
            # Get diagnostic question if tutor_engine is available
            if tutor_engine:
                diagnostic = tutor_engine.get_diagnostic_question(
                    topic=learning_state['currentTopic'],
                    difficulty=learning_state['difficulty']
                )
                learning_state['lastQuestionId'] = diagnostic.get('id', 'd1')
                session['learning_state'] = learning_state
                
                return jsonify({
                    'assistantMessage': f"Great! Let's start fresh. Here's a question to see where you're at:\n\n{diagnostic['question']}",
                    'stateUpdate': learning_state,
                    'practice': [{
                        'id': diagnostic.get('id', 'd1'),
                        'question': diagnostic['question'],
                        'answerType': diagnostic['answerType']
                    }],
                    'quiz': [],
                    'plan7Days': []
                })
            else:
                return jsonify({
                    'assistantMessage': "Great! Let's start fresh. What Algebra topic would you like to work on?",
                    'stateUpdate': learning_state,
                    'practice': [],
                    'quiz': [],
                    'plan7Days': []
                })
        
        # Add student message to chat history
        if student_message:
            chat_history.append({'role': 'user', 'content': student_message})
        
        # If we have a last question and student answered, evaluate and tag misconceptions
        if tutor_engine and learning_state.get('lastQuestionId') and student_message:
            # Try to get the expected answer from the last question
            # This would ideally be stored, but for MVP we'll use the diagnostic question
            topic = learning_state.get('currentTopic', 'linear_equations')
            difficulty = learning_state.get('difficulty', 'core')
            
            # Get the question data to evaluate
            diagnostic = tutor_engine.get_diagnostic_question(topic, difficulty)
            
            # Evaluate answer and tag misconceptions
            evaluation = tutor_engine.update_state_from_student_answer(
                topic=topic,
                student_answer=student_message,
                expected_signals={
                    'correctAnswer': diagnostic.get('correctAnswer', ''),
                    'question': diagnostic.get('question', ''),
                    'difficulty': difficulty
                }
            )
            
            # Update weak areas with new misconceptions
            if evaluation.get('misconceptions'):
                weak_areas = learning_state.get('weakAreas', [])
                for mis in evaluation['misconceptions']:
                    if mis not in weak_areas:
                        weak_areas.append(mis)
                learning_state['weakAreas'] = weak_areas[:10]  # Limit to 10
            
            # Update mastered if correct
            if evaluation.get('isCorrect'):
                mastery_key = f"{topic}_{difficulty}"
                mastered = learning_state.get('mastered', [])
                if mastery_key not in mastered:
                    mastered.append(mastery_key)
                learning_state['mastered'] = mastered[:10]  # Limit to 10
            
            # Update difficulty based on performance
            if tutor_engine:
                new_difficulty = tutor_engine.choose_difficulty(student_profile, learning_state)
                learning_state['difficulty'] = new_difficulty
            
            # Update stage (simple progression)
            current_stage = learning_state.get('stage', 'diagnostic')
            if current_stage == 'diagnostic' and evaluation.get('isCorrect'):
                learning_state['stage'] = 'teach'
            elif current_stage == 'teach':
                learning_state['stage'] = 'practice'
            
            session['learning_state'] = learning_state
        
        # Get topic data for prompt building
        topic_data = {}
        if tutor_engine:
            topic_data = tutor_engine.topic_data
        else:
            # Fallback: load topic data directly
            try:
                with open('data/algebra_topics.json', 'r', encoding='utf-8') as f:
                    topic_data = json.load(f)
                    # Build lookup dicts
                    topic_data['topicNames'] = {}
                    topic_data['topicById'] = {}
                    for topic in topic_data.get('topics', []):
                        if isinstance(topic, dict) and 'id' in topic:
                            topic_data['topicNames'][topic['id']] = topic.get('label', topic['id'])
                            topic_data['topicById'][topic['id']] = topic
            except Exception:
                topic_data = {'topics': [], 'topicNames': {}, 'topicById': {}, 'misconceptionLabels': {}}
        
        # Build prompt
        prompt = build_tutor_prompt(
            student_profile=student_profile,
            student_message=student_message or "Let's continue",
            mode=mode,
            chat_history=chat_history,
            topic_data=topic_data,
            learning_state=learning_state
        )

        # Call Gemini
        try:
            response_text = gemini_client.generate_text(prompt)
        except Exception as e:
            # API call failed
            return jsonify({
                'error': str(e),
                **create_safe_fallback_response(learning_state, student_message)
            }), 500
        
        # Parse JSON robustly
        response = parse_json_robust(response_text)
        
        if not response:
            # Parsing failed - return safe fallback
            return jsonify(create_safe_fallback_response(learning_state, student_message))
        
        # Validate and normalize response structure
        if 'stateUpdate' not in response:
            response['stateUpdate'] = learning_state
        else:
            # Update learning state from response, but preserve stage and lastQuestionId
            current_stage = learning_state.get('stage', 'diagnostic')
            current_question_id = learning_state.get('lastQuestionId')
            learning_state.update(response['stateUpdate'])
            # Preserve stage and lastQuestionId if not in response
            if 'stage' not in response.get('stateUpdate', {}):
                learning_state['stage'] = current_stage
            if 'lastQuestionId' not in response.get('stateUpdate', {}):
                learning_state['lastQuestionId'] = current_question_id
            session['learning_state'] = learning_state
        
        # Ensure all required fields are present
        result = {
            'assistantMessage': response.get('assistantMessage', "Let's continue learning!"),
            'stateUpdate': learning_state,
            'practice': response.get('practice', []),
            'quiz': response.get('quiz', []),
            'plan7Days': response.get('plan7Days', [])
        }
        
        # Add assistant message to chat history
        if result['assistantMessage']:
            chat_history.append({'role': 'assistant', 'content': result['assistantMessage']})
            session['chat_history'] = chat_history[-20:]  # Keep last 20 messages
        
        return jsonify(result)
        
    except Exception as e:
        # Unexpected error - return safe fallback
        return jsonify({
            'error': str(e),
            **create_safe_fallback_response(session.get('learning_state', {}), student_message)
        }), 500


# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'gemini_client_ready': gemini_client is not None,
        'tutor_engine_ready': tutor_engine is not None
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
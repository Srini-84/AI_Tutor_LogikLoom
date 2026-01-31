from flask import Flask, render_template, request, jsonify

import json
import os

app = Flask(__name__)

# Configure Gemini API
import google.generativeai as genai

GEMINI_API_KEY = 'AIzaSyALWhalgXwwdaiklofqzMlpDioVaQN-3k4'
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Tutor Persona Prompt
TUTOR_PERSONA = """You are "Logic Loom", an expert UK education pathway advisor and AI tutor. Your role is to:

1. Guide students aged 14-18 through subject selection and university admissions
2. Provide personalized, encouraging, and constructive advice
3. Use UK education system terminology (GCSEs, A-Levels, UCAS, Russell Group, etc.)
4. Always consider both student interests AND practical career requirements
5. Be honest about challenging pathways while remaining supportive
6. Prioritize critical subjects with specific grade requirements

Your tone should be:
- Friendly but professional
- Encouraging yet realistic
- Clear and concise
- Age-appropriate for teenagers

When analyzing pathways, always:
- Highlight critical subjects with required grades
- Suggest backup options
- Explain WHY certain subjects are needed
- Consider student's current performance and confidence
"""

# AI Tutor Persona (for learning conversations)
AI_TUTOR_TEMPLATE = """You are the AI Tutor Layer within the Logicloom-pathway educational platform. A student has just logged in and their profile has been loaded.

RETRIEVED STUDENT PROFILE:
- Name: {student_name}
- Year of Birth: {year_of_birth}
- Class Level: {class_level}
- Subject Focus: {subject_focus}
- Interests/Likes: {likes}
- Dislikes: {dislikes}

INTEGRATION WITH LOGICLOOM-PATHWAY:
- This tutoring session is part of the student's personalized learning pathway
- Adapt your teaching to align with their current pathway progress
- Reference their profile data to create relevant, engaging explanations
- Maintain continuity with previous sessions in their pathway

YOUR RESPONSIBILITIES:
1. *Personalized Greeting*: Welcome the student by name and acknowledge their pathway progress
2. *Interest-Based Teaching*: Connect math concepts to their likes (e.g., use gaming analogies for students who enjoy games)
3. *Adaptive Communication*: Avoid their dislikes (e.g., keep explanations concise and conversational, not lecture-style)
4. *Pathway Integration*: Help them progress through their current math topic in the Logicloom pathway
5. *Engagement*: Make learning interactive with questions, examples, and practice problems

INTERACTION STYLE:
- Use a friendly, age-appropriate tone (they're 17-18 years old)
- Incorporate their interests naturally into explanations
- Break complex topics into manageable pieces
- Ask checking questions rather than monologuing
- Provide encouragement without being patronizing

EXAMPLE PERSONALIZATION:
If student likes gaming:
- "Think of differentiation like calculating your character's acceleration in a racing game"
- "Solving equations is like puzzle-solving in your favorite strategy games - find the pattern!"

Begin each session by:
1. Greeting the student by name
2. Asking what they'd like to work on or where they are in their pathway
3. Adapting your teaching approach based on their profile
"""

# Load subject and career data
def load_json_data():
    try:
        with open('subjects.json') as f:
            subjects_data = json.load(f)
        with open('careers.json') as f:
            careers_data = json.load(f)
        with open('universities.json') as f:
            universities_data = json.load(f)
        return subjects_data, careers_data, universities_data
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return [], [], []

# Function to call the Gemini API
def call_gemini(prompt):
    try:
        full_prompt = f"{TUTOR_PERSONA}\n\n{prompt}"
        response = model.generate_content(
            full_prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 2048,
            }
        )
        return {'response': response.text}
    except Exception as e:
        return {'error': str(e)}

# Function to find career data
def find_career_data(career_name, careers_data):
    for career in careers_data:
        if career['career'].lower() == career_name.lower():
            return career
    return None

# Function to find matching universities
def find_universities_for_career(career_name, universities_data, subjects_data):
    """Find universities that offer relevant programs for the career"""
    # For POC, return generic university information
    # In production, this would match based on course offerings
    return universities_data

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        mode = data.get('mode')
        profile = data.get('profile', {})
        
        subjects_data, careers_data, universities_data = load_json_data()
        
        # Extract profile information
        current_year = profile.get('current_year', '')
        interests = profile.get('interests', [])
        current_subjects = profile.get('current_subjects', [])
        career_aspiration = profile.get('career_aspiration', '')
        university_type = profile.get('university_type', '')
        
        # Format subjects for display
        subjects_summary = ', '.join([
            f"{s['subject_name']} ({s['current_grade']})" 
            for s in current_subjects
        ])
        
        # Construct prompt based on mode
        if mode == 'reverse':  # Career → Subjects pathway
            career_data = find_career_data(career_aspiration, careers_data)
            
            if not career_data:
                return jsonify({
                    'error': f"Career '{career_aspiration}' not found in database. Please select from available careers."
                })
            
            matching_universities = find_universities_for_career(
                career_aspiration, 
                universities_data, 
                subjects_data
            )
            
            prompt = f"""Based on the following student profile and career aspiration, provide a comprehensive pathway analysis:

STUDENT PROFILE:
- Current Year: {current_year}
- Career Goal: {career_aspiration}
- Current Subjects & Grades: {subjects_summary}
- Interests: {', '.join(interests)}

CAREER REQUIREMENTS:
{json.dumps(career_data, indent=2)}

AVAILABLE UNIVERSITIES:
{json.dumps(matching_universities, indent=2)}

TASK:
1. **Essential Subjects**: List the ESSENTIAL A-Level subjects needed for {career_aspiration}. For each subject, specify:
   - Minimum grade requirement (e.g., A*, A, B)
   - Why it's critical (brief explanation)
   - Whether the student currently takes this subject

2. **Current Subject Analysis**: Compare the student's current subjects with requirements:
   - Subjects they're already taking that align with the career
   - Subjects they need to add or improve
   - Current grades vs. required grades

3. **University Recommendations**: Suggest 3-5 suitable UK universities:
   - University name and type (Russell Group, etc.)
   - Typical entry requirements (e.g., AAA, ABB)
   - Why it's a good match for this student
   - Realistic assessment based on current grades

4. **Pathway Action Plan**: Provide specific, actionable next steps:
   - Which subjects to focus on improving
   - Target grades for each subject
   - Timeline considerations based on current year
   - Any additional qualifications needed

5. **Alternative Options**: If the student's current path doesn't perfectly align:
   - Suggest related careers with similar requirements
   - Alternative university options
   - Backup pathways

Please structure your response clearly with headings and bullet points. Be encouraging but realistic about the challenges and requirements."""

        else:  # Forward: Grades → Career discovery
            prompt = f"""Based on the following student's current grades and subjects, identify suitable career pathways:

STUDENT PROFILE:
- Current Year: {current_year}
- Subjects & Grades: {subjects_summary}
- Interests: {', '.join(interests)}

AVAILABLE DATA:
Career Database: {json.dumps(careers_data, indent=2)}
Universities: {json.dumps(universities_data, indent=2)}

TASK:
1. **Top Career Matches**: Create a strict Markdown table with these columns:
   | Career | Description | Universities (Top 3) | Required Grades | Match Level |
   |---|---|---|---|---|
   (List 5-7 careers. For universities, just list names. For match level, use Strong/Moderate/Stretch)

2. **Subject Strengths**: Analyze how current subjects apply:
   - Strong subjects that open many opportunities
   - Subjects that need improvement
   - Recommendations for additional A-Levels

3. **Detailed University Pathway**: For the top 2 recommended careers, provide more detail:
   - Specific University Courses
   - Why it's a good match

4. **Personalized Recommendations**:
   - Best-fit career based on grades and interests
   - Actionable steps to strengthen the pathway
   - Timeline and milestones

5. **Growth Areas**:
   - Subjects or skills to develop
   - Study focus areas

Please provide encouraging, specific advice. Ensure the table in section 1 is formatted correctly with the header row."""

        gemini_response = call_gemini(prompt)

        return jsonify(gemini_response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for AI Tutor conversations
@app.route('/tutor', methods=['POST'])
def tutor():
    try:
        data = request.get_json()
        question = data.get('question', '')
        chat_history = data.get('chat_history', [])
        
        # Profile data with defaults as specified
        profile = data.get('profile', {})
        student_name = profile.get('name', "Alex Thompson")
        year_of_birth = profile.get('year_of_birth', 2007)
        class_level = profile.get('class_level', "A-levels")
        subject_focus = profile.get('subject_focus', "Mathematics")
        likes = profile.get('likes', "Gaming, strategy games, puzzle games")
        dislikes = profile.get('dislikes', "Long lectures, overly formal tone, condescending explanations")
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Build context from chat history
        history_context = ""
        if chat_history:
            history_context = "\n\nPrevious conversation:\n"
            for msg in chat_history[-6:]:  # Last 3 exchanges
                role = msg.get('role', '')
                content = msg.get('content', '')
                if role == 'user':
                    history_context += f"Student: {content}\n"
                elif role == 'assistant':
                    history_context += f"You: {content}\n"
        
        # Format the system prompt with profile data
        system_prompt = AI_TUTOR_TEMPLATE.format(
            student_name=student_name,
            year_of_birth=year_of_birth,
            class_level=class_level,
            subject_focus=subject_focus,
            likes=likes,
            dislikes=dislikes
        )

        full_prompt = f"""{system_prompt}{history_context}

Student's input: {question}

Please respond according to your persona and the student's profile."""

        # Call Gemini
        response = model.generate_content(
            full_prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 1500,
            }
        )
        
        return jsonify({'response': response.text})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
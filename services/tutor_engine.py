"""Tutor engine for adaptive Algebra tutoring with Socratic method."""
import json
import os
import re
from typing import Dict, Any, List, Optional


class TutorEngine:
    """Manages adaptive tutoring logic, difficulty, and misconception tracking."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize tutor engine. API key is optional (not used here, kept for compatibility)."""
        self.topic_data = {}
        self.load_topics()
    
    def load_topics(self) -> bool:
        """
        Load algebra topics data safely with error handling.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            # Try to find the file in different possible locations
            possible_paths = [
                'data/algebra_topics.json',
                os.path.join(os.path.dirname(__file__), '..', 'data', 'algebra_topics.json'),
                os.path.join(os.getcwd(), 'data', 'algebra_topics.json')
            ]
            
            topic_data = None
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        topic_data = json.load(f)
                    break
            
            if not topic_data:
                raise FileNotFoundError("algebra_topics.json not found in any expected location")
            
            # Validate and normalize structure
            if 'topics' not in topic_data:
                raise ValueError("Missing 'topics' key in algebra_topics.json")
            
            # Build lookup dictionaries
            topic_data['topicNames'] = {}
            topic_data['diagnostics'] = {}
            topic_data['topicById'] = {}
            
            for topic in topic_data['topics']:
                if not isinstance(topic, dict) or 'id' not in topic:
                    continue
                
                topic_id = topic['id']
                topic_data['topicNames'][topic_id] = topic.get('label', topic_id)
                topic_data['topicById'][topic_id] = topic
                
                # Extract diagnostics
                if 'diagnostics' in topic:
                    topic_data['diagnostics'][topic_id] = topic['diagnostics']
            
            # Ensure misconceptionLabels exists
            if 'misconceptionLabels' not in topic_data:
                topic_data['misconceptionLabels'] = {}
            
            self.topic_data = topic_data
            return True
            
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self._create_fallback_data()
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            self._create_fallback_data()
            return False
        except Exception as e:
            print(f"Error loading topic data: {e}")
            self._create_fallback_data()
            return False
    
    def _create_fallback_data(self):
        """Create minimal fallback data structure."""
        self.topic_data = {
            'topics': [],
            'topicNames': {},
            'diagnostics': {},
            'misconceptionLabels': {},
            'topicById': {}
        }
    
    def choose_difficulty(self, student_profile: Dict[str, Any], state: Dict[str, Any]) -> str:
        """
        Choose appropriate difficulty level based on student profile and current state.
        
        Args:
            student_profile: Student setup data (confidence, grade_year, etc.)
            state: Current learning state (weakAreas, mastered, etc.)
        
        Returns:
            Difficulty level: 'foundation', 'core', or 'higher'
        """
        confidence = student_profile.get('confidence', 3)
        weak_areas = state.get('weakAreas', [])
        mastered = state.get('mastered', [])
        current_difficulty = state.get('difficulty', 'core')
        
        # If student has many weak areas, move down
        if len(weak_areas) > 3:
            if current_difficulty == 'higher':
                return 'core'
            elif current_difficulty == 'core':
                return 'foundation'
        
        # If student has mastered concepts and few weak areas, move up
        if len(mastered) > 2 and len(weak_areas) <= 1:
            if current_difficulty == 'foundation':
                return 'core'
            elif current_difficulty == 'core':
                return 'higher'
        
        # Base difficulty on confidence if no state history
        if not weak_areas and not mastered:
            if confidence >= 4:
                return 'higher'
            elif confidence >= 2:
                return 'core'
            else:
                return 'foundation'
        
        # Otherwise maintain current difficulty
        return current_difficulty
    
    def get_diagnostic_question(self, topic: str, difficulty: str) -> Dict[str, Any]:
        """
        Get diagnostic question for a topic at specified difficulty.
        
        Args:
            topic: Topic ID (e.g., 'linear_equations')
            difficulty: 'foundation', 'core', or 'higher'
        
        Returns:
            Dict with question, answerType, correctAnswer, difficulty
        """
        # Get topic data
        topic_obj = self.topic_data.get('topicById', {}).get(topic)
        if not topic_obj:
            # Fallback to first topic if not found
            topics = self.topic_data.get('topics', [])
            if topics and isinstance(topics[0], dict):
                topic_obj = topics[0]
                topic = topic_obj.get('id', 'linear_equations')
            else:
                # Ultimate fallback
                return {
                    'question': 'Solve: x + 2 = 5',
                    'answerType': 'short',
                    'correctAnswer': 'x = 3',
                    'difficulty': 'foundation',
                    'id': 'fallback_1'
                }
        
        diagnostics = topic_obj.get('diagnostics', {})
        if not diagnostics:
            diagnostics = self.topic_data.get('diagnostics', {}).get(topic, {})
        
        # Get diagnostic for specified difficulty, fallback to foundation
        diagnostic = diagnostics.get(difficulty) or diagnostics.get('foundation', {})
        
        return {
            'question': diagnostic.get('question', ''),
            'answerType': diagnostic.get('answerType', 'short'),
            'correctAnswer': diagnostic.get('correctAnswer', ''),
            'difficulty': difficulty,
            'id': f"{topic}_{difficulty}_diagnostic"
        }
    
    def update_state_from_student_answer(
        self,
        topic: str,
        student_answer: str,
        expected_signals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update state based on student answer with lightweight heuristic tagging.
        
        Args:
            topic: Topic ID
            student_answer: Student's answer text
            expected_signals: Dict with 'correctAnswer', 'question', 'difficulty', etc.
        
        Returns:
            Updated state dict with misconceptions tagged
        """
        correct_answer = expected_signals.get('correctAnswer', '')
        question = expected_signals.get('question', '')
        difficulty = expected_signals.get('difficulty', 'core')
        
        # Normalize answers for comparison
        student_clean = self._normalize_answer(student_answer)
        correct_clean = self._normalize_answer(correct_answer)
        
        is_correct = student_clean == correct_clean
        
        # Tag misconceptions using heuristics
        misconceptions = []
        if not is_correct:
            misconceptions = self._tag_misconceptions(topic, student_answer, question, correct_answer)
        
        return {
            'isCorrect': is_correct,
            'misconceptions': misconceptions
        }
    
    def _normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison (remove spaces, lowercase, etc.)."""
        if not answer:
            return ''
        # Remove spaces, lowercase, remove common formatting
        normalized = answer.strip().lower()
        normalized = re.sub(r'\s+', '', normalized)
        # Remove equals signs and common separators for comparison
        normalized = normalized.replace('=', '').replace('x', 'x').replace('y', 'y')
        return normalized
    
    def _tag_misconceptions(
        self,
        topic: str,
        student_answer: str,
        question: str,
        correct_answer: str
    ) -> List[str]:
        """
        Tag misconceptions using simple heuristics.
        
        Returns:
            List of misconception labels
        """
        misconceptions = []
        student_lower = student_answer.lower()
        question_lower = question.lower()
        
        if topic == 'solving_inequalities':
            # Check for sign flip issues with negatives
            if ('-' in question_lower or 'negative' in question_lower) and '>' in question_lower:
                # If question has negative coefficient and inequality, check if sign was flipped
                if '<' in student_lower and '>' in question_lower:
                    # Student might have flipped correctly, but check if answer is wrong
                    if not self._answers_match(student_answer, correct_answer):
                        misconceptions.append('sign_flip_with_negatives')
                elif '>' in student_lower and '<' in question_lower:
                    # Sign direction changed but might be wrong
                    misconceptions.append('sign_flip_with_negatives')
            
            # Check for inequality direction errors
            if ('<' in question_lower and '>' in student_lower) or ('>' in question_lower and '<' in student_lower):
                misconceptions.append('inequality_direction_errors')
        
        elif topic == 'expanding_brackets':
            # Check if only first term was multiplied (incomplete distribution)
            # Simple heuristic: if answer has fewer terms than expected
            expected_terms = len(re.findall(r'[+-]?\s*\d*[xy]?\d*', correct_answer))
            student_terms = len(re.findall(r'[+-]?\s*\d*[xy]?\d*', student_answer))
            if student_terms < expected_terms - 1:  # Allow some variance
                misconceptions.append('distribution_incomplete')
            
            # Check for missing multiplication of all terms
            if '(' in question and ')' in question:
                # Count terms in brackets
                bracket_content = re.search(r'\(([^)]+)\)', question)
                if bracket_content:
                    bracket_terms = len(re.findall(r'[+-]', bracket_content.group(1))) + 1
                    if student_terms < bracket_terms:
                        misconceptions.append('distribution_incomplete')
        
        elif topic == 'factorisation':
            # Check for missing common factor
            # If question has numbers and answer doesn't show common factor extraction
            if re.search(r'\d+', question) and not re.search(r'\d+\s*\(', student_answer):
                misconceptions.append('missing_common_factors')
            
            # Check for wrong factor pairs (for quadratics)
            if '^2' in question or 'x²' in question:
                # Check if answer has two factors
                factors = re.findall(r'\([^)]+\)', student_answer)
                if len(factors) != 2:
                    misconceptions.append('wrong_factor_pairs')
        
        elif topic == 'simultaneous_equations':
            # Check for elimination sign mistakes
            # If student answer has wrong signs in intermediate steps (hard to detect from final answer)
            # Simple check: if answer format is wrong (missing comma, wrong format)
            if ',' not in student_answer and ',' in correct_answer:
                misconceptions.append('elimination_sign_mistakes')
            
            # Check for no substitution back (if only one variable provided)
            variables = re.findall(r'[xy]\s*=', student_answer)
            if len(variables) < 2 and ',' in correct_answer:
                misconceptions.append('no_substitution_back')
        
        elif topic == 'linear_equations':
            # Check for inverse operations confusion
            # If student has wrong sign in answer compared to question
            question_nums = re.findall(r'-?\d+', question)
            answer_nums = re.findall(r'-?\d+', student_answer)
            if question_nums and answer_nums:
                # Simple check: if signs are consistently wrong
                question_has_neg = any(int(n) < 0 for n in question_nums)
                answer_has_neg = any(int(n) < 0 for n in answer_nums if n.lstrip('-').isdigit())
                if question_has_neg != answer_has_neg and not self._answers_match(student_answer, correct_answer):
                    misconceptions.append('inverse_operations_confusion')
            
            # Check for sign errors (positive/negative confusion)
            if self._has_sign_error(student_answer, correct_answer):
                misconceptions.append('sign_errors')
        
        # Always add general misconceptions if answer is wrong
        if not misconceptions:
            misconceptions.append('arithmetic_errors')
        
        return misconceptions
    
    def _answers_match(self, answer1: str, answer2: str) -> bool:
        """Check if two answers match (normalized comparison)."""
        return self._normalize_answer(answer1) == self._normalize_answer(answer2)
    
    def _has_sign_error(self, student_answer: str, correct_answer: str) -> bool:
        """Check if answer has sign errors (opposite signs)."""
        # Extract numbers from answers
        student_nums = re.findall(r'-?\d+', student_answer)
        correct_nums = re.findall(r'-?\d+', correct_answer)
        
        if not student_nums or not correct_nums:
            return False
        
        # Check if numbers are opposite signs
        try:
            student_val = int(student_nums[0])
            correct_val = int(correct_nums[0])
            # Check if opposite signs
            if (student_val > 0 and correct_val < 0) or (student_val < 0 and correct_val > 0):
                return abs(student_val) == abs(correct_val)  # Same magnitude, opposite sign
        except (ValueError, IndexError):
            pass
        
        return False
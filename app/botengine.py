import re
import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.gemini_key)
model = genai.GenerativeModel('gemini-pro')

HALLUCINATION_TRIGGERS = {
    "uncertainty": ["I think", "maybe", "perhaps", "not sure"],
    "generic": ["as an AI", "language model", "cannot answer"],
    "irrelevant": ["however", "completely different", "unrelated"]
}

def validate_user_input(user_input, current_step, context=None):
    """
    Validate user input based on the current step using LLM
    Returns: (is_valid: bool, validation_message: str)
    """
    validation_prompt = f"""
    You are a validation assistant for a hiring process. Your task is to:
    1. Validate if the user input is appropriate for the current step
    2. Provide constructive feedback if the input is invalid
    3. Return results in a specific format

    Current Step: {current_step}
    User Input: {user_input}
    Context: {context}

    Return your response in this exact format:
    VALID: <true/false>
    MESSAGE: <validation message>

    Rules:
    - For names: Must be at least 2 words, no special characters
    - For emails: Must follow standard email format
    - For OTP: Must be exactly 6 digits
    - For phone numbers: Must include country code
    - For experience: Must be a number between 0-30
    - For positions: Must be one of the standard positions
    - For tech stack: Must contain relevant technical terms
    - For interview answers: Must be relevant to the question
    """
    
    try:
        response = model.generate_content(validation_prompt).text
        is_valid = "VALID: true" in response
        message = response.split("MESSAGE: ")[1].strip()
        return is_valid, message
    except Exception as e:
        print(f"Validation error: {e}")
        return False, "Sorry, I'm having trouble validating your input. Please try again."

def is_relevant_response(question, answer, threshold=0.7):
    prompt = f"""Analyze if this answer addresses the question. Return 1 if relevant, 0 if irrelevant:
    
    Question: {question}
    Answer: {answer}
    
    Output only 1 or 0:"""
    
    try:
        response = model.generate_content(prompt).text.strip()
        return int(response) == 1
    except:
        return len(answer) > 20  # Fallback check

def detect_hallucination(text):
    text = text.lower()
    for category in HALLUCINATION_TRIGGERS.values():
        if any(trigger in text for trigger in category):
            return True
    return False

def generate_questions(tech_stack, position):
    prompt = f"""Generate 3 technical interview questions for a {position} position requiring {tech_stack}:
    1. Basic concept question
    2. Intermediate problem-solving question
    3. Advanced system design/scenario question
    
    Format: Separate questions with '|||'"""
    
    response = model.generate_content(prompt).text
    return [q.strip() for q in response.split("|||")[:3]]

def evaluate_answer(question, answer):
    evaluation_prompt = f"""Evaluate this technical answer on a scale of 0-10:
    
    Question: {question}
    Answer: {answer}
    
    Consider:
    - Technical accuracy (40%)
    - Completeness (30%)
    - Clarity (20%)
    - Best practices (10%)
    
    Provide only the numerical score:"""
    
    try:
        response = model.generate_content(evaluation_prompt).text
        return min(max(int(response.strip()), 0), 10)
    except:
        return 5  # Fallback average score
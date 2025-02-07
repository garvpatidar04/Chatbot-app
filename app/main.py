import random
import time
import streamlit as st
from utils import is_valid_email, send_email
from botengine import generate_questions, evaluate_answer, validate_user_input

# Streamlit App Structure
st.set_page_config(page_title="TalentScout", layout="centered")
st.title("TalentScout Hiring Assistant")

# Injecting Custom CSS for Styling
st.markdown("""
    <style>
        /* Custom Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="st-"] {
            font-family: 'Poppins', sans-serif;
        }

        button:hover {
            background-color: #1D4ED8 !important;
        }
        
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "otp_verified" not in st.session_state:
        st.session_state.otp_verified = False
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "tech_questions" not in st.session_state:
        st.session_state.tech_questions = []
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "interview_finished" not in st.session_state:
        st.session_state.interview_finished = False 

# Initialize session state
initialize_session_state()


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to add a message to the chat
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)

# Function to handle OTP verification
def verify_otp(otp_input):
    if int(otp_input) == st.session_state.otp:
        st.session_state.otp_verified = True
        add_message("assistant", "Email verified successfully!")
        return True
    else:
        add_message("assistant", "Invalid OTP. Please try again.")
        return False

# Function to redirect to current question
def redirect_to_question():
    if st.session_state.interview_started:
        ask_question()
    else:
        current_step = get_current_step()
        add_message("assistant", f"Let's continue from where we left off, {current_step['prompt']}")

# Function to get current step information
def get_current_step():
    steps = {
        "name": {
            "prompt": "What is your full name?",
            "validation": "Please provide a valid full name (2+ words, no special characters)"
        },
        "email": {
            "prompt": "Please provide your email address.",
            "validation": "Please enter a valid email address"
        },
        "otp": {
            "prompt": "Please enter the 6-digit OTP sent to your email.",
            "validation": "Please enter a valid 6-digit OTP"
        },
        "phone": {
            "prompt": "Please provide your phone number with country code.",
            "validation": "Please enter a valid phone number"
        },
        "experience": {
            "prompt": "How many years of experience do you have?",
            "validation": "Please enter a number between 0 and 30"
        },
        "position": {
            "prompt": "Which position are you applying for?",
            "validation": "Please select from available positions"
        },
        "tech_stack": {
            "prompt": "Please list your technical skills.",
            "validation": "Please provide your technical skills"
        }
    }
    
    if st.session_state.interview_started:
        return {
            "prompt": f"Q{st.session_state.current_question_index + 1}: {st.session_state.tech_questions[st.session_state.current_question_index]}",
            "validation": "Please provide a relevant answer to the question"
        }
    
    if not st.session_state.user_data.get("name"):
        return steps["name"]
    elif not st.session_state.user_data.get("email"):
        return steps["email"]
    elif not st.session_state.otp_verified:
        return steps["otp"]
    elif not st.session_state.user_data.get("phone"):
        return steps["phone"]
    elif not st.session_state.user_data.get("experience"):
        return steps["experience"]
    elif not st.session_state.user_data.get("position"):
        return steps["position"]
    elif not st.session_state.user_data.get("tech_stack"):
        return steps["tech_stack"]
    else:
        return {"prompt": "How can I assist you further?", "validation": ""}

# Function to start the interview
def start_interview():
    st.session_state.interview_started = True
    st.session_state.tech_questions = generate_questions(
        st.session_state.user_data['tech_stack'],
        st.session_state.user_data['position']
    )
    st.session_state.answers = [""] * len(st.session_state.tech_questions)
    st.session_state.current_question_index = 0
    ask_question()

# Function to ask the current question
def ask_question():
    question = st.session_state.tech_questions[st.session_state.current_question_index]
    add_message("assistant", f"Q{st.session_state.current_question_index + 1}: {question}")

# Function to handle user input
def handle_user_input(user_input):
    # ----- Modification 1: Skip LLM input validation for interview question answers -----
    if st.session_state.interview_started:
        # Directly record the answer (even if it is "no") and move to the next question.
        st.session_state.answers[st.session_state.current_question_index] = user_input
        st.session_state.current_question_index += 1
        if st.session_state.current_question_index < len(st.session_state.tech_questions):
            ask_question()
        else:
            evaluate_interview()
        return  # Skiping further processing and validation for interview answers.
    
    # For non-interview steps, continue with LLM validation.
    current_step = get_current_step()
    
    # Validate input using LLM (only for candidate details, not interview answers because they can be vague)
    is_valid, validation_message = validate_user_input(
        user_input=user_input,
        current_step=current_step["prompt"],
        context=st.session_state.user_data
    )
    
    if not is_valid:
        add_message("assistant", validation_message)
        redirect_to_question()
        return
    
    # Process valid input for candidate details
    if not st.session_state.user_data.get("name"):
        st.session_state.user_data["name"] = user_input
        add_message("assistant", "Great! What is your email address?")
    elif not st.session_state.user_data.get("email"):
        if is_valid_email(user_input):
            st.session_state.user_data["email"] = user_input
            otp = random.randint(100000, 999999)
            st.session_state.otp = otp
            if send_email(
                recipient_email=user_input,
                subject="Email Verification OTP",
                body=f"Your OTP for email verification is: {otp}"
            ):
                add_message("assistant", "OTP sent to your email. Please check your inbox.")
            else:
                add_message("assistant", "Failed to send OTP. Please try again.")
        else:
            add_message("assistant", "Invalid email address. Please enter a valid email.")
    elif not st.session_state.otp_verified:
        if verify_otp(user_input):
            add_message("assistant", "Please enter your phone number.")
    elif not st.session_state.user_data.get("phone"):
        st.session_state.user_data["phone"] = user_input
        add_message("assistant", "How many years of experience do you have?")
    elif not st.session_state.user_data.get("experience"):
        try:
            st.session_state.user_data["experience"] = int(user_input)
            add_message("assistant", "Which position are you applying for?")
        except ValueError:
            add_message("assistant", "Please enter a valid number for years of experience.")
    elif not st.session_state.user_data.get("position"):
        st.session_state.user_data["position"] = user_input
        add_message("assistant", "What is your tech stack? (e.g., Python, Django, React, SQL)")
    elif not st.session_state.user_data.get("tech_stack"):
        st.session_state.user_data["tech_stack"] = user_input
        add_message("assistant", "Thank you! Let's start the interview.")
        start_interview()
    else:
        # For any extra non-interview input
        add_message("assistant", "How can I assist you further?")

# Function to evaluate the interview
def evaluate_interview():
    st.session_state.score = 0
    for i, (q, answer) in enumerate(zip(st.session_state.tech_questions, st.session_state.answers)):
        evaluation = evaluate_answer(q, answer)
        try:
            score = int(evaluation)
            st.session_state.score += score
        except ValueError:
            add_message("assistant", f"Error: Unable to determine score for Q{i+1}. Please try again.")
    add_message("assistant", f"Thank you for completing the interview. Your score is {st.session_state.score}.")
    send_result_email()
    st.session_state.interview_finished = True

# Function to send the result email
def send_result_email():
    candidate_email = st.session_state.user_data.get("email", "")
    if candidate_email:
        if st.session_state.score > 18:
            subject = "Congratulations! You are selected for the next round"
            body = (
                "Dear Candidate,\n\n"
                "Congratulations! Based on your performance in the technical interview, you have been selected for the next round of the hiring process.\n"
                "Our HR team will reach out to you within 48 hours with further details.\n\n"
                "Best Regards,\nTalentScout Hiring Team"
            )
        else:
            subject = "Update on Your Interview Process"
            body = (
                "Dear Candidate,\n\n"
                "We appreciate your time and effort in participating in our technical interview process. Unfortunately, we regret to inform you that you have not been selected to move forward in the hiring process at this time.\n"
                "We encourage you to apply again in the future and wish you the best of luck in your career endeavors.\n\n"
                "Best Regards,\nTalentScout Hiring Team"
            )
        
        email_sent = send_email(candidate_email, subject, body)
        if email_sent:
            add_message("assistant", "For Furthure details, Email has been sent to you please check that.")
        else:
            add_message("assistant", "Failed to send email. Please try again later.")

# ----- Main Chat Input Area -----
if st.session_state.get("interview_finished"):
    st.markdown("## Thank You!")
    st.markdown("Thank you for participating in the interview. We will be in touch with you soon.")
else:
    if prompt := st.chat_input("Type your response here..."):
        add_message("user", prompt)
        handle_user_input(prompt)

# Initial message 
if not st.session_state.messages:
    add_message(
        "assistant",
        "Welcome to TalentScout Hiring Assistant! 🎉 \
        I'm here to help you assess your eligibility for the job with a quick interview. \
        Let's get started! \
        \n\nCould you please share your full name?"
    )
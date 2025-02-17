import os
import streamlit as st
import nest_asyncio
import textwrap
import random
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory

# Allow nested asyncio loops for Streamlit compatibility
nest_asyncio.apply()

# -------------------------------
# 🔷 Streamlit Page Configuration
# -------------------------------
st.set_page_config(page_title="Multi-Type Quiz Generator", layout="wide")
st.title("AI-Powered Quiz Generator")
st.markdown("This app generates quizzes with **randomized question types** for young students.")



# 🔷 Sidebar: API Key Setup
# -------------------------------
st.sidebar.header("🔑 API Key Setup")
aiml_api_key = st.sidebar.text_input("Enter your AIML API Key", type="password")
if aiml_api_key:
    os.environ["AIML_API_KEY"] = aiml_api_key
else:
    st.sidebar.warning("⚠️ Please enter your AIML API key to proceed.")
    st.stop()

st.sidebar.success("✅ API Key Set.")

# -------------------------------
# 🔷 Model Creation Functions
# -------------------------------
def create_deepseek_model():
    """Creates and returns a DeepSeek-67B model for AI tasks."""
    return ModelFactory.create(
        model_platform=ModelPlatformType.AIML,
        model_type=ModelType.DEEPSEEK_CHAT,
        api_key=aiml_api_key
    )

# -------------------------------
# 🔷 Define AI Agents
# -------------------------------
def create_teacher_agent():
    """Creates the Teacher Agent responsible for quiz generation."""
    teacher_msg = BaseMessage.make_assistant_message(
        role_name="Teacher",
        content=textwrap.dedent("""\
            🎓 You are a Teacher generating a quiz for young students.

            ✅ **Task:**  
            - Generate a **quiz with 5 questions**.  
            - Each question must have a **different format** from:  
                Multiple Choice
                Fill in the Blank  

            🎯 **Rules:**  
            - Each question should test **a different math concept**.  
            - Do not add other format of question.
            - Include **correct answers** for each question.
            - keep the Possible answers list and the correct answers list simple, dont add any additional thing like A) 12,B) 20 etc
            - Strings in a list should be double quoted
            - Follow this format:
            ---
            **Question Type:** 
            **Question Description:** 
            **Possible Answers:** []  
            **Correct Answer:** [] 
            --- 
        """)
    )
    return ChatAgent(system_message=teacher_msg, model=create_deepseek_model())

# -------------------------------
# 🔷 Generate a Quiz with Varied Question Types
# -------------------------------
def generate_quiz(subject,level):
    """Generates a quiz with varied question types using the AI teacher agent."""
    teacher_agent = create_teacher_agent()
    quiz_prompt = "Generate a quiz with 5 questions for {subject} at an education level of {level}, each having a different format (MCQ ,Fill in the Blank)."
    
    response = teacher_agent.step(quiz_prompt)
    return response.msg.content

# -------------------------------
# 🔷 Extract Questions & Answers
# -------------------------------
def parse_list(list_string):
    try:
        # Safely convert the string to a list using eval
        result = eval(list_string)
        if isinstance(result, list):
            return result
        else:
            return []
    except Exception as e:
        print(f"Error parsing list: {e}")
        return []
    
def extract_questions_and_answers(quiz_content):
    """Extracts questions, answers, and correct answers from structured AI-generated quiz content."""
    questions = []
    question_blocks = quiz_content.split("\n---\n")

    for block in question_blocks:
        question_data = {"answers": [], "correct_answer": []}

        lines = block.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("**Question Type:**"):
                question_data["type"] = line.replace("**Question Type:**", "").strip()

            elif line.startswith("**Question Description:**"):
                question_data["questiondesc"] = line.replace("**Question Description:**", "").strip()

            elif line.startswith("**Possible Answers:**"):
                match = line.replace("**Possible Answers:**", "").strip()
                possible_answers = parse_list(match)
                question_data["answers"] = possible_answers  # Store as list without labels

            # Extract Correct Answer (just a list without labels)
            elif line.startswith("**Correct Answer:**"):
                match = line.replace("**Correct Answer:**", "").strip()
                correct_answer = parse_list(match)
                question_data["correct_answer"] = correct_answer  # Store as list without labels

        questions.append(question_data)
    return questions

# -------------------------------
# 🔷 Handle Answer Input Based on Question Type
# -------------------------------
# Update this function to handle unique keys for each question
def handle_answer_input(question, disabled=False):
    """Displays correct input method based on question type."""
    # Unique key for each question type
    question_key = f"{st.session_state.question_idx}_{question['type']}"

    if question["type"] == "Multiple Choice":
        # Ensure the key is unique per question and disable if necessary
        selected_answer = st.radio("Choose an answer:", question["answers"], key=f"mcq_{question_key}", disabled=disabled)
        return selected_answer

    elif question["type"] == "Drag and Drop":
        # Ensure the key is unique per question and disable if necessary
        selected_answer = st.multiselect("Arrange in order:", question["answers"], key=f"dragdrop_{question_key}", disabled=disabled)
        return selected_answer

    elif question["type"] == "Fill in the Blank":
        # Ensure the key is unique per question and disable if necessary
        selected_answer = st.text_input("Fill in the blank:", key=f"fill_{question_key}", disabled=disabled).strip()
        return selected_answer

# -------------------------------
# 🔷 Move to Next Question
# -------------------------------
def next_question():
    """Move to the next question"""
    if st.session_state.question_idx < len(st.session_state.questions) - 1:
        st.session_state.question_idx += 1  # Update the index directly
        st.session_state.answered = False  # Reset answered state
        st.session_state.correct_answers.append(None)  # Add placeholder for next question's answer
    st.rerun()  # Trigger a re-render
# -------------------------------
# 🔷 Move to Previous Question
# -------------------------------
def previous_question():
    """Move to the previous question"""
    if st.session_state.question_idx > 0:
        st.session_state.question_idx -= 1  # Update the index directly
        st.session_state.answered = False  # Reset answered state
    st.rerun()  # Trigger a re-render
    
# Track the correct and incorrect answers
# -------------------------------
# 🔷 Check Answer
# -------------------------------
def check_answer(user_answer, correct_answer, question):
    """Checks the user's answer against the correct answer and provides feedback."""
    # Track the result for each question
    if str(user_answer) == str(correct_answer):
        st.session_state.correct_answers.append(True)
        st.success("✅ Correct!")
    elif isinstance(correct_answer, list):
        if str(user_answer) in correct_answer:
            st.success("✅ Correct!")
            st.session_state.correct_answers.append(True)
        else:
            st.session_state.correct_answers.append(False)
            st.error(f"❌ Incorrect. Correct answer(s): {correct_answer}, your answer: {user_answer}")
    else:
        st.session_state.correct_answers.append(False)
        st.error(f"❌ Incorrect. Correct answer: {correct_answer}, your answer: {user_answer}")
    print(st.session_state.correct_answers)
# -------------------------------
# 🔷 Show the Result
# -------------------------------
def show_result():
    """Shows the result page after finishing the quiz."""
    if not st.session_state.quiz_finished:
        return  # Ensure that the result page isn't shown unless the quiz is finished

    correct_count = st.session_state.correct_answers.count(True)
    total_count = len(st.session_state.correct_answers)
    cleaned_list = list(filter(lambda x: x is not None, st.session_state.correct_answers))
    
    st.markdown("## 🎉 Quiz Finished! 🎉")
    st.markdown(f"**You answered {correct_count} out of {total_count} questions correctly!**")
    
    # Display feedback for each question
    for idx, (question, correct) in enumerate(zip(st.session_state.questions, cleaned_list), 1):
        st.markdown(f"### **Question {idx}:** {question['questiondesc']}")
        st.markdown(f"**Your Answer:** {question['user_answer']}")

        if correct:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer: {question['correct_answer']}")

        st.markdown("---")

# Handle the quiz completion
# Update finish_quiz function
def finish_quiz():
    """Finishes the quiz and shows the result page."""
    if st.session_state.question_idx == len(st.session_state.questions) - 1:
        st.session_state.quiz_finished = True  # Mark the quiz as finished
        st.session_state.answered = True  # Ensure that we do not allow the user to move forward
        st.session_state.correct_answers.append(None)  # Placeholder for the last question's answer
        st.rerun()  # Force the page to re-run and show the result immediately
        
def start_interactive_quiz():
    """Ensures quiz remains visible and handles answer checking."""
    if "question_idx" not in st.session_state:
        st.session_state.question_idx = 0
        st.session_state.answered = False
        st.session_state.correct_answers = []
    
    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False
    
    questions = st.session_state.questions
    if not questions:
        st.warning("No questions found! Generate a quiz first.")
        return

    current_question = questions[st.session_state.question_idx]
    
    if 'user_answer' not in current_question:
        current_question['user_answer'] = None

    total_questions = len(st.session_state.questions)
    progress = st.session_state.question_idx / total_questions
    st.progress(progress)

    st.markdown(f"### Question {st.session_state.question_idx + 1}")
    st.markdown(f"**{current_question['questiondesc']}**")

    disabled = st.session_state.answered
    user_answer = handle_answer_input(current_question, disabled)

    if st.session_state.question_idx < len(st.session_state.questions):
        current_question['user_answer'] = user_answer

    submit_answer_button = st.button("Submit Answer", disabled=disabled, key="submit_answer")

    if submit_answer_button and user_answer is not None:
        st.session_state.answered = True
        check_answer(user_answer, current_question["correct_answer"], current_question)

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.question_idx > 0:
            if st.button("Previous Question", key="previous_question"):
                previous_question()

    with col2:
        if st.session_state.question_idx == len(st.session_state.questions) - 1:
            if st.button("Finish Quiz", key="finish_quiz"):
                finish_quiz()  # Finish the quiz after the last question
        else:
            next_button_disabled = not st.session_state.answered
            if st.button("Next Question", disabled=next_button_disabled, key="next_question"):
                next_question()

    if st.session_state.quiz_finished:
        show_result()

# -------------------------------
# 🔷 Landing Page for Quiz Generation & Interaction
# -------------------------------
def landing_page():
    """Displays the landing page to generate and interact with quizzes."""
    # Initialize session state variables if not already initialized
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "correct_answers" not in st.session_state:
        st.session_state.correct_answers = []
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "question_idx" not in st.session_state:
        st.session_state.question_idx = 0
    if "quiz_text" not in st.session_state:
        st.session_state.quiz_text = ""
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    # Subject and Education Level selection
    subject = st.selectbox("Select Subject", ["Mathematics", "Science", "History", "Geography", "English"])
    education_level = st.selectbox("Select Education Level", ["Primary", "Secondary", "High School"])

    # First, check if the user wants to generate a new quiz or interact with the current one
    if st.button("Generate New Quiz"):
        st.session_state.quiz_text = generate_quiz(subject, education_level)  # Generate quiz with selected subject and level
        questions = extract_questions_and_answers(st.session_state.quiz_text)  # Extract questions and answers
        st.session_state.questions = questions  # Save the questions in session state

    # Display the interactive quiz if questions are already available
    if st.session_state.questions:
        start_interactive_quiz()
# -------------------------------
# 🔷 Run the Application
# -------------------------------
landing_page()

import streamlit as st
import pandas as pd
import random

# Initialize session state variables
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'incorrect_answers' not in st.session_state:
    st.session_state.incorrect_answers = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'current_answer' not in st.session_state:
    st.session_state.current_answer = None
if 'selected_range' not in st.session_state:
    st.session_state.selected_range = (1, 10)
if 'feedback' not in st.session_state:
    st.session_state.feedback = None

# List of motivational phrases
motivational_phrases = [
    "### 🎉 Fantastic! Keep it up! 🎉",
    "### 🌟 Awesome job! You’re a star! 🌟",
    "### 👏 Way to go! You nailed it! 👏",
    "### 👍 Great work! Keep shining! 👍",
    "### 🎈 Superb! You’re amazing! 🎈",
    "### 🥳 Excellent! Keep rocking! 🥳",
    "### 💪 You did it! So proud of you! 💪",
    "### ✨ Wonderful! You’re doing great! ✨",
    "### 🎊 Brilliant! Keep the streak going! 🎊",
    "### 🏅 Outstanding! You’re on fire! 🏅"
]


# Function to generate a new question
def new_question(range_min, range_max):
    table = random.randint(range_min, range_max)
    num = random.randint(1, 10)
    question = f"{table} x {num}"
    answer = table * num
    return question, answer


# Title and introduction
st.title("Bianca's Multiplication Party 😸")
st.write(
    "Welcome to the multiplication game! Choose a range of tables, answer the questions, and see how many you can get right! 😊")

# Range slider for selecting the multiplication table range
selected_range = st.slider("Select a range of multiplication tables to practice:", 1, 10, (1, 10))

# Generate a new question if the selected range has changed or if there's no current question
if st.session_state.selected_range != selected_range or st.session_state.current_question is None:
    st.session_state.selected_range = selected_range
    st.session_state.current_question, st.session_state.current_answer = new_question(*selected_range)
    st.session_state.feedback = None

# Display the current question
st.markdown(f"## 🤔 Question: {st.session_state.current_question}")

# Input field for the answer
user_answer = st.text_input("Your answer:", key='answer_input')

# Button to submit the answer
if st.button("Submit"):
    try:
        if int(user_answer) == st.session_state.current_answer:
            st.session_state.correct_answers += 1
            st.balloons()
            st.session_state.feedback = random.choice(motivational_phrases)
        else:
            st.session_state.incorrect_answers += 1
            st.session_state.feedback = f"### 😔 Incorrect. The answer was {st.session_state.current_answer}. Try the next one!"

        # Generate a new question after submitting an answer
        st.session_state.current_question, st.session_state.current_answer = new_question(
            *st.session_state.selected_range)
        # Clear the input field
        st.rerun()
    except ValueError:
        st.error("Please enter a valid number.")

# Display feedback
if st.session_state.feedback:
    st.markdown(st.session_state.feedback)

# Display the score table in a dataframe
score_data = {
    '✅ Correct Answers': [st.session_state.correct_answers],
    '❌ Incorrect Answers': [st.session_state.incorrect_answers]
}

st.divider()
score_df = pd.DataFrame(score_data)
st.write("### 🥇 Score")
st.dataframe(score_df, hide_index=True)

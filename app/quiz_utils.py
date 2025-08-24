import random
import streamlit as st

def get_quiz_questions(dataset, num=5):
    # Ensure dataset is a list of questions (strings)
    if isinstance(dataset, dict):
        questions = list(dataset.values())
    elif isinstance(dataset, set):
        questions = sorted(list(dataset))
    else:
        questions = list(dataset)
    if not questions:
        return []
    return random.sample(questions, min(num, len(questions)))

def quiz_engine(questions):
    if "quiz_index" not in st.session_state:
        st.session_state["quiz_index"] = 0
    if "quiz_answers" not in st.session_state:
        st.session_state["quiz_answers"] = [None] * len(questions)

    idx = st.session_state["quiz_index"]
    question = questions[idx]
    st.markdown(f"**Question {idx+1} of {len(questions)}:** {question}")
    user_answer = st.text_input("Your Answer:", key=f"quiz_answer_{idx}")

    if st.button("Submit Answer", key=f"submit_{idx}"):
        st.session_state["quiz_answers"][idx] = user_answer
        st.success("Answer saved!")

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous", key="prev") and idx > 0:
            st.session_state["quiz_index"] -= 1
    with col2:
        if st.button("Next", key="next") and idx < len(questions)-1:
            st.session_state["quiz_index"] += 1

    # Show feedback if answered
    if st.session_state["quiz_answers"][idx] is not None:
        st.info(f"Your answer: {st.session_state['quiz_answers'][idx]}")

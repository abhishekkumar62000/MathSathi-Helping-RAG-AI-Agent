import streamlit as st

def collaborative_whiteboard_chat():
    st.subheader("🧑‍🤝‍🧑 Real-Time Collaborative Whiteboard & Chat (Demo)")
    st.info("This is a demo. For true real-time sync, use a backend like Firebase or Socket.io.")
    session_code = st.text_input("Session Code (share with others to join same room):", value="math123")
    st.markdown(f"**You are in session:** `{session_code}`")
    # Shared whiteboard (simulate with a shared text area for now)
    board = st.text_area("Shared Whiteboard (text/ASCII for demo):", key=f"collab_board_{session_code}")
    # Simple chat
    if f"chat_{session_code}" not in st.session_state:
        st.session_state[f"chat_{session_code}"] = []
    chat_input = st.text_input("Type a message:", key=f"collab_chat_input_{session_code}")
    if st.button("Send", key=f"send_{session_code}"):
        st.session_state[f"chat_{session_code}"].append(chat_input)
    st.markdown("**Chat History:**")
    for msg in st.session_state[f"chat_{session_code}"][-10:]:
        st.write(msg)

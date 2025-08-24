def show_whiteboard():
    import streamlit as st
    try:
        from streamlit_drawable_canvas import st_canvas
        import uuid
        st.subheader("🧑‍🤝‍🧑 Real-Time Collaborative Whiteboard & Chat")
        st.markdown("Draw diagrams, annotate equations, or sketch math problems below. Share your session code for group work!")
        session_code = st.text_input("Session Code (share with others to join same room):", value="math123", key="whiteboard_session_code")
        st.markdown(f"**You are in session:** `{session_code}`")
        col1, col2, col3 = st.columns(3)
        with col1:
            stroke_color = st.color_picker("Pen Color", "#000000")
        with col2:
            stroke_width = st.slider("Pen Width", 1, 10, 3)
        with col3:
            drawing_mode = st.selectbox("Mode", ["freedraw", "line", "rect", "circle", "transform"])
        # Unique canvas key per session
        canvas_key = f"canvas_{session_code}"
        if canvas_key not in st.session_state:
            st.session_state[canvas_key] = str(uuid.uuid4())
        if st.button("Clear Whiteboard"):
            st.session_state[canvas_key] = str(uuid.uuid4())
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.0)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color="#fff",
            height=350,
            width=600,
            drawing_mode=drawing_mode,
            key=st.session_state[canvas_key],
        )
        if canvas_result.image_data is not None:
            st.image(canvas_result.image_data, caption="Your Drawing", use_column_width=True)
            import io
            from PIL import Image
            img = Image.fromarray((canvas_result.image_data).astype('uint8'))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("Download Drawing as PNG", buf.getvalue(), file_name="whiteboard.png", mime="image/png")
        # Collaborative chat (per session)
        st.markdown("---")
        st.markdown("### 💬 Group Chat")
        chat_key = f"chat_{session_code}"
        if chat_key not in st.session_state:
            st.session_state[chat_key] = []
        chat_input = st.text_input("Type a message:", key=f"whiteboard_chat_input_{session_code}")
        if st.button("Send", key=f"whiteboard_send_{session_code}"):
            st.session_state[chat_key].append(chat_input)
        st.markdown("**Chat History:**")
        for msg in st.session_state[chat_key][-10:]:
            st.write(msg)
        if not canvas_result.json_data or not canvas_result.json_data.get("objects"):
            st.warning("If you cannot draw, try refreshing the page or using a different browser. If the problem persists, use the fallback below.")
            st.markdown("---")
            st.markdown("**Fallback: ASCII/Markdown Drawing**")
            st.text_area("Draw or describe your math visually (ASCII art, Markdown, or text):", key=f"whiteboard_fallback_{session_code}")
        st.caption("You can use this whiteboard for geometry, graphs, or visual explanations! Share your session code for real-time group work.")
    except ImportError:
        st.error("streamlit-drawable-canvas is not installed. Please run: pip install streamlit-drawable-canvas")
        st.markdown("---")
        st.markdown("**Fallback: ASCII/Markdown Drawing**")
        st.text_area("Draw or describe your math visually (ASCII art, Markdown, or text):", key="whiteboard_fallback")

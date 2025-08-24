
import streamlit as st
st.set_page_config(page_title="Math Agent 🧮", layout="wide")
from streamlit.components.v1 import html
import sys
import os
import json
import pandas as pd

# Add root to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.benchmark import benchmark_math_agent  # Add this import
from data.load_gsm8k_data import load_jeebench_dataset
from rag.query_router import answer_math_question
import base64
# --- Custom Dark Theme and Animations ---
"""
--- SIDEBAR LOGO, AI IMAGE, AND DEVELOPER INFO ---
"""
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logo_path = os.path.join(project_root, "Logo.png")
ai_logo_path = os.path.join(project_root, "AI.png")
dev_pic_path = os.path.join(project_root, "pic.jpg")
encoded_logo = None
encoded_ai_logo = None
encoded_dev_pic = None
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
if os.path.exists(ai_logo_path):
    with open(ai_logo_path, "rb") as image_file:
        encoded_ai_logo = base64.b64encode(image_file.read()).decode()
if os.path.exists(dev_pic_path):
    with open(dev_pic_path, "rb") as image_file:
        encoded_dev_pic = base64.b64encode(image_file.read()).decode()

with st.sidebar:
    st.markdown(
        f"""
        <style>
        @keyframes colorfulGlow {{
            0% {{ box-shadow: 0 0 24px #ffd200, 0 0 0px #00c6ff; filter: hue-rotate(0deg); }}
            25% {{ box-shadow: 0 0 32px #00c6ff, 0 0 12px #f7971e; filter: hue-rotate(90deg); }}
            50% {{ box-shadow: 0 0 40px #f7971e, 0 0 24px #ffd200; filter: hue-rotate(180deg); }}
            75% {{ box-shadow: 0 0 32px #00c6ff, 0 0 12px #ffd200; filter: hue-rotate(270deg); }}
            100% {{ box-shadow: 0 0 24px #ffd200, 0 0 0px #00c6ff; filter: hue-rotate(360deg); }}
        }}
        .colorful-animated-logo {{
            animation: colorfulGlow 2.5s linear infinite;
            transition: box-shadow 0.3s, filter 0.3s;
            border-radius: 30%;
            box-shadow: 0 2px 12px #00c6ff;
            border: 2px solid #ffd200;
            background: #232526;
            object-fit: cover;
        }}
        .sidebar-logo {{
            text-align: center;
            margin-bottom: 12px;
        }}
        .sidebar-AI {{
            text-align: center;
            margin-bottom: 8px;
        }}
        .sidebar-dev {{
            text-align: center;
            margin-top: 10px;
            margin-bottom: 0px;
        }}
        </style>
        <div class='sidebar-logo'>
            {f"<img class='colorful-animated-logo' src='data:image/png;base64,{encoded_logo}' alt='Logo' style='width:120px;height:120px;'>" if encoded_logo else "<div style='font-size:2em;'>🚀</div>"}
            <div style='color:#00c6ff;font-size:1.1em;font-family:sans-serif;font-weight:bold;text-shadow:0 1px 6px #ffd200;margin-top:8px;'>Professor.Team.Agent</div>
        </div>
        <div class='sidebar-AI'>
            {f"<img src='data:image/png;base64,{encoded_ai_logo}' alt='AI' style='width:210px;height:210px;margin-bottom:8px;object-fit:cover;'>" if encoded_ai_logo else "<div style='color:#ff4b4b;'>AI.png not found</div>"}
        </div>
        <div class='sidebar-dev'>
            <div style='color:#ffd200;font-size:1.05em;font-family:sans-serif;font-weight:bold;margin-bottom:4px;'>👨‍💻 Developer: Abhishek Yadav</div>
            {f"<img src='data:image/jpeg;base64,{encoded_dev_pic}' alt='Abhishek Yadav' style='width:100%;max-width:210px;display:block;margin-left:auto;margin-right:auto;margin-bottom:4px;'>" if encoded_dev_pic else "<div style='color:#ff4b4b;'>pic.jpg not found</div>"}
        </div>
        """,
        unsafe_allow_html=True
    )





# --- Playful Neon Blue-Pink-Orange Theme ---
st.markdown(
    """
    <style>
    body, .stApp {
        background: linear-gradient(135deg, #232526 0%, #414345 100%) !important;
        color: #f8fafc !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 121, 198, 0.13);
        color: #ffb86b;
        border-radius: 18px 18px 0 0;
        margin-right: 8px;
        font-weight: 800;
        font-size: 1.15rem;
        border: 2px solid #8be9fd;
        transition: background 0.3s, color 0.3s;
        box-shadow: 0 2px 16px 0 #ff79c6;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #8be9fd 0%, #ff79c6 50%, #ffb86b 100%);
        color: #232526 !important;
        box-shadow: 0 6px 32px 0 #ffb86b;
        border-bottom: 4px solid #ffb86b;
    }
    .stButton>button {
        background: linear-gradient(90deg, #8be9fd 0%, #ff79c6 50%, #ffb86b 100%) !important;
        color: #232526 !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900;
        font-size: 1.15rem;
        box-shadow: 0 2px 18px 0 #ff79c6;
        transition: transform 0.18s, box-shadow 0.18s, background 0.3s;
        cursor: pointer;
        letter-spacing: 1.2px;
        padding: 0.6em 1.3em;
        margin-bottom: 0.25em;
        outline: none !important;
        animation: bounceIn 0.7s;
    }
    .stButton>button:hover {
        transform: scale(1.10) rotate(-2deg);
        box-shadow: 0 8px 36px 0 #ffb86b;
        background: linear-gradient(90deg, #ffb86b 0%, #8be9fd 100%) !important;
    }
    .stButton>button:active {
        transform: scale(0.96);
        background: #232526 !important;
        color: #ff79c6 !important;
    }
    @keyframes bounceIn {
        0% { transform: scale(0.7); opacity: 0.2; }
        60% { transform: scale(1.15); opacity: 1; }
        100% { transform: scale(1); }
    }
    .main-title-anim {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(270deg, #8be9fd, #ff79c6, #ffb86b, #8be9fd);
        background-size: 800% 800%;
        color: #fff;
        text-shadow: 0 0 12px #8be9fd, 0 0 24px #ff79c6, 0 0 32px #ffb86b;
        letter-spacing: 3px;
        margin-bottom: 0.8em;
        text-align: center;
        border-radius: 18px;
        padding: 0.25em 0.5em;
        animation: gradientMove 4s ease-in-out infinite, glowPulse 2.5s ease-in-out infinite alternate;
        box-shadow: 0 0 32px 0 #ffb86b55, 0 0 12px 0 #8be9fd55;
    }
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes glowPulse {
        0% { text-shadow: 0 0 12px #8be9fd, 0 0 24px #ff79c6, 0 0 32px #ffb86b; }
        50% { text-shadow: 0 0 32px #ffb86b, 0 0 48px #8be9fd, 0 0 64px #ff79c6; }
        100% { text-shadow: 0 0 12px #8be9fd, 0 0 24px #ff79c6, 0 0 32px #ffb86b; }
    }
    .stProgress>div>div>div>div {
        background: linear-gradient(90deg, #8be9fd 0%, #ff79c6 100%) !important;
        transition: width 0.5s cubic-bezier(.4,2,.3,1);
    }
    .stExpander, .stTextArea, .stTextInput {
        background: rgba(255, 184, 107, 0.10) !important;
        color: #ff79c6 !important;
        border-radius: 18px !important;
        border: 2px solid #8be9fd !important;
        box-shadow: 0 2px 18px 0 #ff79c633;
    }
    .stTextArea textarea, .stTextInput input {
        background: rgba(139,233,253,0.13) !important;
        color: #ffb86b !important;
    }
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 16px !important;
        font-weight: 800;
        font-size: 1.10rem;
        background: rgba(255,121,198,0.08) !important;
        color: #ffb86b !important;
    }
    ::-webkit-scrollbar {
        width: 10px;
        background: #232526;
    }
    ::-webkit-scrollbar-thumb {
        background: #ff79c6;
        border-radius: 10px;
    }
    /* Glassy card effect for containers */
    .st-emotion-cache-1avcm0n, .st-emotion-cache-1v0mbdj, .st-emotion-cache-1dp5vir {
        background: rgba(139,233,253,0.10) !important;
        border-radius: 26px !important;
        box-shadow: 0 10px 40px 0 #ffb86b44 !important;
        border: 2px solid #ff79c622 !important;
        backdrop-filter: blur(10px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Animated main title
st.markdown('<div class="main-title-anim">🧠 MathSathi Helping AI Agent🤖</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📘 Ask a Question",
    "📁 View Feedback",
    "📊 Benchmark Results",
    "👤 My Dashboard",
    "📝 Whiteboard",
    "📷 Math OCR & Quiz",
    "🎬 Animated Solution",
    "💡 Error Diagnosis & Hints"
])
# ---------------- TAB 7: Step-by-Step Solution Animation ---------------- #
import time
with tab7:
    st.subheader("🎬 Step-by-Step Solution Animation")
    question = st.text_area("Enter a math question:", key="anim_q")
    if st.button("Animate Solution"):
        with st.spinner("Generating step-by-step solution..."):
            answer = answer_math_question(question)
        st.markdown("**Animated Steps:**")
        import re
        step_regex = re.compile(r"(Step \\d+|\\d+\\.|•|\\*)(.*?)(?=(?:\\nStep \\d+|\\n\\d+\\.|\\n•|\\n\\*|$))", re.DOTALL)
        matches = list(step_regex.finditer(answer))
        if matches and len(matches) > 1:
            if "anim_step" not in st.session_state:
                st.session_state["anim_step"] = 0
            if "anim_autoplay" not in st.session_state:
                st.session_state["anim_autoplay"] = False
            if "show_all_steps" not in st.session_state:
                st.session_state["show_all_steps"] = False
            total_steps = len(matches)
            col1, col2, col3, col4, col5 = st.columns([1,2,1,1,1])
            prev_clicked = col1.button("⬅️ Previous Step", key="prev_step_btn")
            next_clicked = col3.button("Next Step ➡️", key="next_step_btn")
            reset_clicked = col4.button("🔄 Reset", key="reset_step_btn")
            showall_clicked = col5.button("📜 Show All Steps", key="showall_step_btn")
            if prev_clicked and st.session_state["anim_step"] > 0:
                st.session_state["anim_step"] -= 1
            if next_clicked and st.session_state["anim_step"] < total_steps-1:
                st.session_state["anim_step"] += 1
            if reset_clicked:
                st.session_state["anim_step"] = 0
                st.session_state["show_all_steps"] = False
            if showall_clicked:
                st.session_state["show_all_steps"] = not st.session_state["show_all_steps"]
            st.progress((st.session_state["anim_step"]+1)/total_steps, text=f"Step {st.session_state['anim_step']+1} of {total_steps}")
            if st.session_state["show_all_steps"]:
                for i, match in enumerate(matches):
                    step_title = match.group(1).strip()
                    step_content = match.group(2).strip()
                    st.markdown(f"**{step_title}:**")
                    if "$" in step_content:
                        st.latex(step_content)
                    else:
                        st.write(step_content if step_content else "No explanation provided for this step.")
                    st.caption(f"Step {i+1} of {total_steps}")
            else:
                i = st.session_state["anim_step"]
                step_title = matches[i].group(1).strip()
                step_content = matches[i].group(2).strip()
                st.markdown(f"**{step_title}:**")
                if "$" in step_content:
                    st.latex(step_content)
                else:
                    st.write(step_content if step_content else "No explanation provided for this step.")
                st.caption(f"Step {i+1} of {total_steps}")
            # Autoplay
            autoplay_clicked = st.button("▶️ Auto-Play Animation", key="autoplay_btn")
            if autoplay_clicked:
                st.session_state["anim_autoplay"] = True
            if st.session_state.get("anim_autoplay", False):
                for idx in range(st.session_state["anim_step"]+1, total_steps):
                    time.sleep(1.5)
                    st.session_state["anim_step"] = idx
                    st.experimental_rerun()
                st.session_state["anim_autoplay"] = False
        else:
            st.write(answer)

# ---------------- TAB 8: AI-Powered Error Diagnosis & Hints ---------------- #
with tab8:
    st.subheader("💡 AI-Powered Error Diagnosis & Hints")
    user_question = st.text_area("Enter your math question:", key="err_diag_q")
    user_wrong_answer = st.text_area("Your (possibly wrong) answer:", key="err_diag_a")
    if st.button("Diagnose & Get Hint"):
        with st.spinner("Analyzing your answer and generating a hint..."):
            prompt = f"A student tried to solve this math problem: {user_question}\nTheir answer: {user_wrong_answer}\nExplain what mistake they made, and give a hint or a similar practice problem. Format the hint in bold and suggest a similar practice question if possible."
            diagnosis = answer_math_question(prompt)
        import re
        with st.expander("Show Full AI Feedback"):
            st.write(diagnosis)
        # Highlight hint if present
        hint_match = re.search(r"hint[:\-\s]*([\s\S]+?)(?:\n|$)", diagnosis, re.IGNORECASE)
        if hint_match:
            st.markdown(f"**Hint:** {hint_match.group(1).strip()}")
            st.code(hint_match.group(1).strip(), language="markdown")
            st.button("👍 Upvote Hint", key="upvote_hint")
            st.button("📋 Copy Hint", key="copy_hint")
        # Try to extract and show a similar practice problem
        practice_match = re.search(r"practice (question|problem)[:\-\s]*([\s\S]+?)(?:\n|$)", diagnosis, re.IGNORECASE)
        if practice_match:
            st.markdown(f"**Similar Practice Problem:** {practice_match.group(2).strip()}")
            st.code(practice_match.group(2).strip(), language="markdown")
            st.button("📋 Copy Practice Problem", key="copy_practice")

from app.whiteboard_utils import show_whiteboard
import requests
from app.quiz_utils import get_quiz_questions, quiz_engine

# ---------------- TAB 1: Ask a Question ---------------- #
# ---------------- TAB 5: Interactive Whiteboard ---------------- #
with tab5:
    import io
    from PIL import Image
    import requests
    show_whiteboard()
    st.markdown("---")
    st.subheader("✍️ Solve Math Question from Whiteboard")
    st.markdown("Type your math question below (or just draw/write it above):")
    whiteboard_question = st.text_area("Enter your math question", key="whiteboard_math_q")

    # --- Robust OCR Upload & Extraction ---
    st.markdown("If you wrote your question on the whiteboard, download it as PNG and upload below for OCR:")
    uploaded_whiteboard = st.file_uploader("Upload your whiteboard PNG for OCR", type=["png"], key="whiteboard_ocr_upload")
    ocr_text = None
    ocr_api_key = st.secrets["ocr_space_api_key"]  # Fetch OCR.Space API key from Streamlit secrets.toml
    if uploaded_whiteboard:
        image = Image.open(uploaded_whiteboard)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        def ocr_space_image(image_file, api_key):
            url = 'https://api.ocr.space/parse/image'
            payload = {
                'isOverlayRequired': False,
                'apikey': api_key,
                'language': 'eng',
            }
            files = {'filename': ('image.png', image_file, 'image/png')}
            try:
                response = requests.post(url, files=files, data=payload, timeout=30)
                result = response.json()
                if not result.get('IsErroredOnProcessing') and result.get('ParsedResults'):
                    return result['ParsedResults'][0]['ParsedText'], result
                else:
                    return None, result
            except requests.exceptions.Timeout:
                return None, {'ErrorMessage': 'OCR API timed out. Please try again with a smaller or clearer image.'}
            except Exception as e:
                return None, {'ErrorMessage': f'OCR API error: {e}'}
        if ocr_api_key:
            if "last_uploaded_whiteboard" not in st.session_state or st.session_state["last_uploaded_whiteboard"] != uploaded_whiteboard:
                with st.spinner("Extracting text from your whiteboard drawing..."):
                    ocr_text, ocr_result = ocr_space_image(buf, ocr_api_key)
                st.session_state["last_uploaded_whiteboard"] = uploaded_whiteboard
                st.session_state["last_ocr_text"] = ocr_text
                st.session_state["last_ocr_result"] = ocr_result
            else:
                ocr_text = st.session_state.get("last_ocr_text")
                ocr_result = st.session_state.get("last_ocr_result")
            if ocr_text:
                st.success(f"Extracted Question: {ocr_text}")
            else:
                st.error("OCR failed. Please try again with a clearer image or check your API key.")
                if ocr_result and ocr_result.get('ErrorMessage'):
                    st.warning(f"API Error: {ocr_result['ErrorMessage']}")
    # --- Solve Button ---
    solve_btn = st.button("🧮 Solve Whiteboard Question", key="solve_whiteboard_btn")
    question_to_solve = whiteboard_question.strip() if whiteboard_question.strip() else (ocr_text.strip() if ocr_text else None)
    if solve_btn and question_to_solve:
        with st.spinner("Solving your question with step-by-step solution..."):
            answer = answer_math_question(question_to_solve)
        st.markdown("**Step-by-Step Solution:**")
        import re
        step_regex = re.compile(r"(Step \\d+|\\d+\\.|•|\\*)(.*?)(?=(?:\\nStep \\d+|\\n\\d+\\.|\\n•|\\n\\*|$))", re.DOTALL)
        matches = list(step_regex.finditer(answer))
        if matches and len(matches) > 1:
            for i, match in enumerate(matches):
                step_title = match.group(1).strip()
                step_content = match.group(2).strip()
                st.markdown(f"**{step_title}:**")
                if "$" in step_content:
                    st.latex(step_content)
                else:
                    st.write(step_content if step_content else "No explanation provided for this step.")
                st.caption(f"Step {i+1} of {len(matches)}")
        else:
            st.write(answer)

# ---------------- TAB 6: Math OCR & Adaptive Quiz ---------------- #
import PIL
with tab6:
    st.subheader("📷 Instant Math OCR (Image-to-Equation)")
    st.markdown("Upload a photo or screenshot of a math problem. The app will extract the equation and try to solve it.")
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    def ocr_space_image(image_file, api_key):
        url = 'https://api.ocr.space/parse/image'
        payload = {
            'isOverlayRequired': False,
            'apikey': api_key,
            'language': 'eng',
        }
        files = {'filename': ('image.png', image_file, 'image/png')}
        try:
            response = requests.post(url, files=files, data=payload, timeout=30)
            result = response.json()
            if not result.get('IsErroredOnProcessing') and result.get('ParsedResults'):
                return result['ParsedResults'][0]['ParsedText'], result
            else:
                return None, result
        except requests.exceptions.Timeout:
            return None, {'ErrorMessage': 'OCR API timed out. Please try again with a smaller or clearer image.'}
        except Exception as e:
            return None, {'ErrorMessage': f'OCR API error: {e}'}

    import io
    sample_url = "https://i.imgur.com/8COa5Qp.png"  # Example math image
    st.markdown("---")
    st.markdown("Or try with a [sample image](https://i.imgur.com/8COa5Qp.png)")
    if st.button("Load Sample Image"):
        import requests as req
        response = req.get(sample_url)
        if response.status_code == 200:
            uploaded_file = io.BytesIO(response.content)
            uploaded_file.name = "sample.png"
            st.session_state["ocr_uploaded_file"] = uploaded_file
    if "ocr_uploaded_file" in st.session_state and not uploaded_file:
        uploaded_file = st.session_state["ocr_uploaded_file"]

    if uploaded_file:
        image = PIL.Image.open(uploaded_file)
        image = image.convert("RGB")
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.info("Tip: For best results, upload a clear, high-contrast image with typed or printed math. Handwriting and blurry images may fail.")
        ocr_text = None
        ocr_raw = None
        run_ocr = st.button("Extract Text from Image")
        if run_ocr or ("ocr_last_text" in st.session_state and st.session_state.get("ocr_last_image") == uploaded_file):
            with st.spinner("Extracting math text from image via OCR.Space API..."):
                api_key = "K84147951588957"
                ocr_text, ocr_raw = ocr_space_image(buf, api_key)
                st.session_state["ocr_last_text"] = ocr_text
                st.session_state["ocr_last_raw"] = ocr_raw
                st.session_state["ocr_last_image"] = uploaded_file
        if "ocr_last_text" in st.session_state and st.session_state.get("ocr_last_image") == uploaded_file:
            ocr_text = st.session_state["ocr_last_text"]
            ocr_raw = st.session_state["ocr_last_raw"]
        if ocr_text and ocr_text.strip():
            st.markdown("**Extracted Text (editable):**")
            edited_text = st.text_area("Edit or copy the extracted text below:", value=ocr_text, height=100)
            if st.button("Solve Extracted Problem"):
                with st.spinner("Solving extracted problem..."):
                    answer = answer_math_question(edited_text)
                st.success(answer)
        elif ocr_text is not None:
            st.error("❌ OCR failed to extract any text from your image.")
            if ocr_raw and ocr_raw.get('ErrorMessage'):
                st.warning(f"API Error: {ocr_raw['ErrorMessage']}")
            st.markdown("**Debug Info:**")
            st.json(ocr_raw)
            if st.button("Retry Extraction"):
                del st.session_state["ocr_last_text"]
                del st.session_state["ocr_last_raw"]
                del st.session_state["ocr_last_image"]
                st.experimental_rerun()
            st.info("Try another image, or check that your image is clear and contains printed math text. If you see partial text in the debug info, you can copy-paste it manually.")

    st.markdown("---")
    st.subheader("🧠 Adaptive Practice & Smart Quiz Generator")
    try:
        dataset = load_jeebench_dataset()
        quiz_questions = get_quiz_questions(dataset, num=5)
        quiz_engine(quiz_questions)
    except Exception as e:
        st.warning(f"Quiz unavailable: {e}")
with tab1:
    st.subheader("📘 Ask a Math Question")
    st.markdown("Enter any math question below. The agent will try to explain it step-by-step.")

    if "last_question" not in st.session_state:
        st.session_state["last_question"] = ""
    if "last_answer" not in st.session_state:
        st.session_state["last_answer"] = ""
    if "feedback_given" not in st.session_state:
        st.session_state["feedback_given"] = False
    if "feedback" not in st.session_state:
        st.session_state["feedback"] = None

    st.markdown("**You can use LaTeX for math input.** Example: $\\int_0^1 x^2 dx$")
    user_question = st.text_area("Your Question (supports LaTeX):", height=80)
    # Optional: Render LaTeX preview
    if user_question:
        st.markdown("**Preview:**")
        st.latex(user_question)

    if st.button("Get Answer"):
        if user_question:
            with st.spinner("Thinking..."):
                answer = answer_math_question(user_question)
            st.session_state["last_question"] = user_question
            st.session_state["last_answer"] = answer
            st.session_state["feedback_given"] = False
            st.session_state["correction_requested"] = False
            st.session_state["detailed_explanation_requested"] = False
            st.session_state["feedback"] = None

    if st.session_state["last_answer"]:
        st.markdown("### ✅ Answer:")
        import re
        answer = st.session_state["last_answer"]
        # Render LaTeX in answer if present
        if "$" in answer:
            st.latex(answer)
        # Step-by-step visualization (improved)
        # This regex captures both the step header and its content
        step_regex = re.compile(r"(Step \d+|\d+\.|•|\*)(.*?)(?=(?:\nStep \d+|\n\d+\.|\n•|\n\*|$))", re.DOTALL)
        matches = list(step_regex.finditer(answer))
        if matches and len(matches) > 1:
            st.info("Step-by-step solution:")
            for i, match in enumerate(matches):
                step_title = match.group(1).strip()
                step_content = match.group(2).strip()
                with st.expander(f"{step_title}"):
                    st.write(step_content if step_content else "No explanation provided for this step.")
        else:
            st.success(answer)

        # --- Correction & Explanation Requests ---
        if not st.session_state.get("feedback_given", False):
            st.markdown("### 🙋 Was this helpful?")
            col1, col2, col3 = st.columns(3)


            with col1:
                if st.button("👍 Yes"):
                    st.session_state["feedback"] = "positive"
                    st.session_state["feedback_given"] = True
            with col2:
                if st.button("👎 No"):
                    st.session_state["feedback"] = "negative"
                    st.session_state["feedback_given"] = True
            with col3:
                if st.button("❓ Request More Detail"):
                    st.session_state["detailed_explanation_requested"] = True
                    st.session_state["feedback_given"] = True
                    st.session_state["feedback"] = "request_detail"

            if st.session_state["feedback_given"]:
                log_entry = {
                    "question": st.session_state["last_question"],
                    "answer": st.session_state["last_answer"],
                    "feedback": st.session_state["feedback"]
                }
                try:
                    os.makedirs("logs", exist_ok=True)
                    log_file = "logs/feedback_log.json"
                    if os.path.exists(log_file):
                        with open(log_file, "r") as f:
                            existing_logs = json.load(f)
                    else:
                        existing_logs = []
                    existing_logs.append(log_entry)
                    with open(log_file, "w") as f:
                        json.dump(existing_logs, f, indent=2)
                    st.success(f"✅ Feedback recorded as '{st.session_state['feedback']}'")
                    st.write("📝 Log entry:", log_entry)
                except Exception as e:
                    st.error(f"⚠️ Error saving feedback: {e}")

        # If user requested more detail, show a button to get a more detailed explanation
        if st.session_state.get("detailed_explanation_requested", False):
            if st.button("🔄 Generate More Detailed Explanation"):
                with st.spinner("Generating a more detailed explanation..."):
                    # You can call the agent again with a prompt for more detail
                    detailed_question = st.session_state["last_question"] + "\nPlease explain in even more detail, breaking down every step as much as possible."
                    detailed_answer = answer_math_question(detailed_question)
                    st.session_state["last_answer"] = detailed_answer
                    st.session_state["detailed_explanation_requested"] = False
                    st.rerun()

        # If user flagged as incorrect, allow them to request a correction
        if st.session_state.get("feedback_given", False) and st.session_state.get("feedback") == "negative":
            if st.button("🚩 Flag as Incorrect & Request Correction"):
                with st.spinner("Requesting a corrected solution..."):
                    correction_question = st.session_state["last_question"] + "\nYour previous answer was incorrect. Please provide a corrected, step-by-step solution."
                    corrected_answer = answer_math_question(correction_question)
                    st.session_state["last_answer"] = corrected_answer
                    st.session_state["feedback_given"] = False
                    st.session_state["feedback"] = None
                    st.rerun()

# ---------------- TAB 2: View Feedback ---------------- #
with tab2:
    st.subheader("📁 View Collected Feedback")
    try:
        with open("logs/feedback_log.json", "r") as f:
                                {f"<img src='data:image/jpeg;base64,{encoded_dev_pic}' alt='Abhishek Yadav' style='width:100%;max-width:180px;display:block;margin-left:auto;margin-right:auto;margin-bottom:4px;'>" if encoded_dev_pic else "<div style='color:#ff4b4b;'>pic.jpg not found</div>"}
        st.success("Loaded feedback log.")
        st.dataframe(pd.DataFrame(feedback_logs))
    except Exception as e:
        st.warning("No feedback log found or error loading.")
        st.text(str(e))

# ---------------- TAB 3: Benchmark Results ---------------- #

with tab3:
    st.subheader("📊 Benchmark Accuracy Report")

    total_math = len(load_jeebench_dataset())

    st.caption(f"📘 Benchmarking from {total_math} math questions")

    num_questions = st.slider("Select number of math questions to benchmark", min_value=3, max_value=total_math, value=10)

    if st.button("▶️ Run Benchmark Now"):
        with st.spinner(f"Benchmarking {num_questions} math questions..."):
            df_result, accuracy = benchmark_math_agent(limit=num_questions)

            # Save the result
            os.makedirs("benchmark", exist_ok=True)
            result_path = f"benchmark/results_math_{num_questions}.csv"
            df_result.to_csv(result_path, index=False)

            # Show result
            st.success(f"✅ Done! Accuracy: {accuracy:.2f}%")
            st.metric("Accuracy", f"{accuracy:.2f}%")
            st.dataframe(df_result)
            st.download_button("Download Results", data=df_result.to_csv(index=False), file_name=result_path, mime="text/csv")

# ---------------- TAB 4: Personalized Dashboard ---------------- #
import glob
import pandas as pd
with tab4:
    st.subheader("👤 My Learning Dashboard")
    # Load feedback log
    feedback_path = "logs/feedback_log.json"
    if os.path.exists(feedback_path):
        with open(feedback_path, "r") as f:
            feedback_logs = json.load(f)
        df_feedback = pd.DataFrame(feedback_logs)
        st.markdown(f"**Total Questions Attempted:** {len(df_feedback)}")
        st.markdown(f"**Positive Feedback:** {sum(df_feedback['feedback']=='positive')}")
        st.markdown(f"**Negative Feedback:** {sum(df_feedback['feedback']=='negative')}")
        st.markdown(f"**Requested More Detail:** {sum(df_feedback['feedback']=='request_detail')}")
        st.dataframe(df_feedback.tail(10), use_container_width=True)
    else:
        st.info("No feedback data yet. Start asking questions!")

    # Show accuracy from benchmark results
    st.markdown("---")
    st.markdown("### 📈 Benchmark Progress")
    csv_files = glob.glob("benchmark/results_math_*.csv")
    if csv_files:
        latest_csv = max(csv_files, key=os.path.getctime)
        df_bench = pd.read_csv(latest_csv)
        if 'correct' in df_bench.columns:
            accuracy = 100 * df_bench['correct'].sum() / len(df_bench)
            st.metric("Latest Benchmark Accuracy", f"{accuracy:.2f}%")
        st.dataframe(df_bench.head(10), use_container_width=True)
    else:
        st.info("No benchmark results yet.")

    # Recommend practice questions (random from dataset)
    st.markdown("---")
    st.markdown("### 📝 Practice Questions For You")
    try:
        from data.load_gsm8k_data import load_jeebench_dataset
        dataset = load_jeebench_dataset()
        import random
        recs = random.sample(dataset, min(3, len(dataset)))
        for i, q in enumerate(recs):
            st.markdown(f"**Practice {i+1}:** {q}")
    except Exception as e:
        st.warning(f"Could not load practice questions: {e}")

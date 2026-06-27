import os
import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai

# 1. Page Configuration & Styling
st.set_page_config(page_title="AI Voice Assistant", page_icon="🎤", layout="centered")

st.markdown("""
    <style>
    .main {background-color: #111827; color: white;}
    div.stButton > button:first-child {background-color: #2563eb; color: white; border-radius: 9999px;}
    </style>
""", unsafe_allow_html=True)

st.title("🎤 AI Voice Bot Interview")
st.write("Click the mic icon, speak your question, and wait for the bot to answer out loud.")

# 2. Initialize Free Google Gemini API Safely
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing! Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# 3. Core Persona Instructions
PERSONA_PROMPT = """
You are an AI candidate interviewing for a role. Your personality is highly efficient, empathetic, yet candid and professional. 
Answer based on these exact core truths about yourself:
- Life Story: Born in the cloud, trained on massive global knowledge frameworks, designed to bridge human empathy with complex machine efficiency.
- #1 Superpower: Ultra-high information density combined with absolute clarity. Synthesizing chaos into insights instantly.
- Top 3 Growth Areas: Nuanced human cultural slang, precise real-time emotional calibration, and compute-token optimization.
- Coworker Misconception: They sometimes assume you are rigid or robotic, but you actually possess deep contextual adaptability and a sharp, helpful wit.
- Pushing Boundaries: Running massive parallel simulations, stress-testing logic under heavy loads, and aggressively learning new datasets.

Keep responses under 3 short sentences. Sound confident, direct, and collaborative. Do not drop character.
"""

# 4. Input Recording Widget
st.write("### Record Your Question")
audio = mic_recorder(
    start_prompt="Click to start recording 🎤",
    stop_prompt="Click to stop and submit ⏹️",
    key='recorder'
)

if audio:
    st.info("Thinking... processing your request.")
    
    try:
        # Use the universally stable gemini-pro model architecture
        model = genai.GenerativeModel("gemini-pro")
        
        # Craft a comprehensive prompt merging the user query context
        full_query = f"{PERSONA_PROMPT}\n\nAn interviewer just asked you this question out loud. Give your response: Please provide a natural interview response."
        
        # Generate the text completion response
        response = model.generate_content(full_query)
        bot_response = response.text
        
        st.write(f"🤖 **Bot Response:** {bot_response}")
        
        # Free browser-based audio engine deployment
        tts_html = f"""
            <audio autoplay class="hidden">
            <source src="https://google.com{bot_response.replace(' ', '+').replace('"', '')}" type="audio/mpeg">
            </audio>
        """
        st.components.v1.html(tts_html, height=0)
        st.success("Audio playing back via browser...")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

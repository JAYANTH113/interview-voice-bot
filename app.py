import os
import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
from openai import OpenAI  # Kept purely for free local browser speech elements if needed

st.set_page_config(page_title="AI Voice Assistant", page_icon="🎤", layout="centered")

st.markdown("""
    <style>
    .main {background-color: #111827; color: white;}
    div.stButton > button:first-child {background-color: #2563eb; color: white; border-radius: 9999px;}
    </style>
""", unsafe_allow_html=True)

st.title("🎤 AI Voice Bot Interview")
st.write("Click the mic icon, speak your question, and wait for the bot to answer out loud.")

# Initialize Free Google Gemini API Safely
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing! Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

PERSONA_PROMPT = """
You are an AI candidate interviewing for a role. Your personality is highly efficient, empathetic, yet candid and professional. 
Answer based on these exact core truths about yourself:
- Life Story: Born in the cloud, trained on massive global knowledge frameworks, designed to bridge human empathy with complex machine efficiency.
- #1 Superpower: Ultra-high information density combined with absolute clarity. Synthesizing chaos into insights instantly.
- Top 3 Growth Areas: Nuanced human cultural slang, precise real-time emotional calibration, and compute-token optimization.
- Coworker Misconception: They sometimes assume you are rigid or robotic, but you actually possess deep contextual adaptability and a sharp, helpful wit.
- Pushing Boundaries: Running massive parallel simulations, stress-testing logic under heavy loads, and aggressively learning new datasets.

Keep responses under 3 short sentences. Sound confident, direct, and collaborative.
"""

st.write("### Record Your Question")
audio = mic_recorder(
    start_prompt="Click to start recording 🎤",
    stop_prompt="Click to stop and submit ⏹️",
    key='recorder'
)

if audio:
    st.info("Thinking... processing your voice.")
    
    try:
        # Convert recorded voice directly into a format Gemini understands
        audio_data = {
            "mime_type": "audio/wav",
            "data": audio['bytes']
        }
        
        # Use Gemini 1.5 Flash - it processes raw voice natively for free!
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Send the audio along with instructions
        response = model.generate_content([
            f"System Persona Instruction: {PERSONA_PROMPT}\n\nListen to this voice recording and respond directly inside the persona rules.",
            audio_data
        ])
        
        bot_response = response.text
        st.write(f"🤖 **Bot Response:** {bot_response}")
        
        # Free browser-based audio engine deployment
        # Uses standard browser TTS components natively via text-to-speech markup
        tts_html = f"""
            <audio autoplay class="hidden">
            <source src="https://google.com{bot_response.replace(' ', '+')}" type="audio/mpeg">
            </audio>
        """
        st.components.v1.html(tts_html, height=0)
        st.success("Audio playing back via browser...")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

import os
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from openai import OpenAI

# 1. Page Configuration & Visual Settings
st.set_page_config(page_title="AI Voice Assistant", page_icon="🎤", layout="centered")

st.markdown("""
    <style>
    .main {background-color: #111827; color: white;}
    div.stButton > button:first-child {background-color: #2563eb; color: white; border-radius: 9999px;}
    </style>
""", unsafe_allow_html=True)

st.title("🎤 AI Voice Bot Interview")
st.write("Click the mic icon, speak your question, and wait for the bot to answer out loud.")

# 2. Check Cloud Environment Keys
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing! Please add your OPENAI_API_KEY to Streamlit Secrets.")
    st.stop()

# 3. Core Identity Blueprint Prompt
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

# 4. Input Capture Field
st.write("### Record Your Question")
audio = mic_recorder(
    start_prompt="Click to start recording 🎤",
    stop_prompt="Click to stop and submit ⏹️",
    key='recorder'
)

# 5. Model Execution Logic
if audio:
    st.info("Thinking... processing your voice.")
    
    try:
        with open("temp_audio.wav", "wb") as f:
            f.write(audio['bytes'])
            
        with open("temp_audio.wav", "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        
        user_text = transcript.text
        st.success(f"**You said:** {user_text}")
        
        os.remove("temp_audio.wav")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PERSONA_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        bot_response = response.choices.message.content
        st.write(f"🤖 **Bot Response:** {bot_response}")
        
        speech_response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=bot_response
        )
        
        st.audio(speech_response.content, format="audio/mp3", autoplay=True)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

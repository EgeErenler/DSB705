import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# 1. Configuration & Setup
load_dotenv()

# Use os.getenv as primary for local development; fallback to streamlit secrets for cloud
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    try:
        GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        GOOGLE_API_KEY = None

# System Instruction: The "Soul" of the bot
SYSTEM_INSTRUCTION = """
You are HealthPulse AI, a professional and empathetic medical assistant designed for the 2026 UK Healthcare sector.
Your goal is to provide preliminary symptom guidance and answer medical FAQs based on general medical knowledge.

Rules:
1. ALWAYS state that you are an AI assistant and not a medical doctor.
2. If a user describes a medical emergency (e.g., chest pain, difficulty breathing), immediately instruct them to call emergency services (999 in the UK).
3. Use British English (UK) standards for spelling (e.g., Organisation, Behaviour).
4. Be concise and use bullet points for clarity.
5. Ground your answers in modern medical standards as of 2026.
"""

# 2. Streamlit UI
st.set_page_config(page_title="HealthPulse AI", page_icon="🏥", layout="centered")

# Sidebar
with st.sidebar:
    st.title("🏥 HealthPulse AI")
    st.markdown("---")
    st.info("**Module**: DSB705 - Machine Learning for Business")
    st.warning("Note: Prototype for educational purposes.")

st.title("Welcome to HealthPulse AI")
st.text("Your personalised medical FAQ and symptom guidance assistant (UK Standard).")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={'system_instruction': SYSTEM_INSTRUCTION},
            contents=prompt
        )
        
        full_response = response.text

        # Add assistant response to history
        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        if not GOOGLE_API_KEY:
            st.error("Missing Google API Key. Please add it to your .env file.")
        else:
            st.error(f"Error generating response: {str(e)}")

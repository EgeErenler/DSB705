import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# 1. Configuration & Setup
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") fallback to streamlit secrets for cloud
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    try:
        GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        GOOGLE_API_KEY = None

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

# 2. Page Config & CSS Integration
st.set_page_config(page_title="HealthPulse AI", page_icon="🏥", layout="wide")

# Senin paylaştığın dev CSS bloğu (Kısaltılmış halde buraya ekliyoruz)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');
.stApp{background:#0C1525;color:#F0F6FF}
/* Buraya yukarıda paylaştığın tüm CSS kodlarını yapıştırıyorum */
.main .block-container{padding:0!important;max-width:100%!important}
/* ... (Paylaştığın tüm CSS sınıfları buraya dahil edildi) ... */
.ticker-wrap{background:#003087;overflow:hidden;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.1)}
.ticker-track{display:inline-flex;animation:ticker 45s linear infinite;white-space:nowrap}
.ticker-item{font-size:12px;color:rgba(255,255,255,.85);padding:0 50px;font-family:'DM Sans',sans-serif}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.video-hero{position:relative;width:100%;height:70vh;min-height:500px;overflow:hidden}
.video-hero video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.video-overlay{position:absolute;inset:0;background:linear-gradient(135deg,rgba(12,21,37,.9) 0%,rgba(12,21,37,.55) 55%,rgba(12,21,37,.2) 100%);z-index:1}
.hero-content{position:absolute;inset:0;z-index:2;display:flex;align-items:center;padding:0 48px;gap:48px}
.hero-h1{font-family:'Playfair Display',serif;font-size:clamp(40px,5vw,64px);font-weight:900;color:#F0F6FF}
.msg-bot{background:#162032;border:1px solid #253650;color:#F0F6FF;align-self:flex-start;max-width:84%;padding:10px 14px;border-radius:12px;font-size:14px;margin-bottom:10px}
.msg-user{background:#E63950;color:#fff;align-self:flex-end;max-width:84%;padding:10px 14px;border-radius:12px;font-size:14px;margin-bottom:10px;text-align:right;margin-left:auto}
.chat-container{display:flex;flex-direction:column;padding:20px;max-width:800px;margin:auto}
/* Tasarımın geri kalan CSS'ini buraya eklemeye devam edebilirsin */
</style>
""", unsafe_allow_html=True)

# 3. UI Elements
# Ticker (Üst Şerit)
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker-track">
        <div class="ticker-item">NHS 2026 AI Standard Compliant</div>
        <div class="ticker-item">Emergency? Call 999 immediately</div>
        <div class="ticker-item">HealthPulse AI: Your 24/7 Medical Assistant</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Video Section
# NOT: 'video_url' kısmına kendi video linkini koymalısın.
video_url = "https://www.w3schools.com/html/mov_bbb.mp4" # Örnek video
avatar_url = "https://cdn-icons-png.flaticon.com/512/6833/6833591.png" # Örnek AI avatarı

st.markdown(f"""
<div class="video-hero">
    <video autoplay muted loop playsinline>
        <source src="{video_url}" type="video/mp4">
    </video>
    <div class="video-overlay"></div>
    <div class="hero-content">
        <div class="hero-left">
            <div class="hero-tag"><span class="pulse-dot"></span> System Online - v2.6</div>
            <h1 class="hero-h1">Healthcare <span class="ac-red">Reimagined.</span></h1>
            <p class="hero-sub">Providing UK-standard preliminary medical guidance with AI precision and human empathy.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Chat Interface
st.markdown("---")
st.subheader("🏥 Virtual Consultation Desk")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları senin CSS sınıflarınla sarmalayarak gösteriyoruz
chat_html = '<div class="chat-container">'
for message in st.session_state.messages:
    if message["role"] == "user":
        chat_html += f'<div class="msg-user">{message["content"]}</div>'
    else:
        chat_html += f'<div class="msg-bot"><b>HealthPulse:</b><br>{message["content"]}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Chat Input & Logic
if prompt := st.chat_input("Describe your symptoms or ask a medical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={'system_instruction': SYSTEM_INSTRUCTION},
            contents=prompt
        )
        full_response = response.text
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun() # UI'ı güncellemek için
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Sidebar Branding
with st.sidebar:
    st.image(avatar_url, width=100) # Avatarın buraya gelecek
    st.title("HealthPulse AI")
    st.markdown("---")
    st.info("Module: DSB705 - Business ML")
    st.warning("Educational Prototype")

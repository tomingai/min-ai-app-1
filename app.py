import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & FUTURISTISK DESIGN ---
st.set_page_config(page_title="TOMINGAI NEON STUDIO", page_icon="⚡", layout="wide")

# NEON CSS STYLING
st.markdown("""
    <style>
    /* Bakgrund och huvudcontainer */
    .main { background-color: #050505; }
    
    /* Neon Logotyp */
    .neon-wrapper {
        background-color: #0a0a0a;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #00f2ff;
        box-shadow: 0px 0px 20px #00f2ff;
        text-align: center;
        margin-bottom: 40px;
    }
    .neon-text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 50px;
        font-weight: 900;
        color: #fff;
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #00f2ff, 0 0 30px #00f2ff, 0 0 40px #00f2ff;
        margin: 0;
    }
    .neon-sub {
        color: #00f2ff;
        letter-spacing: 5px;
        font-size: 12px;
        text-transform: uppercase;
        margin-top: 10px;
    }
    
    /* Neon Knappar */
    .stButton>button {
        background-color: transparent;
        color: #00f2ff;
        border: 2px solid #00f2ff;
        border-radius: 5px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00f2ff;
        color: black;
        box-shadow: 0px 0px 15px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# Visa den futuristiska logotypen
st.markdown("""
    <div class="neon-wrapper">
        <p class="neon-text">TOMINGAI</p>
        <p class="neon-sub">A.I. NEON ENGINE // VERSION 2.0</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. LOGIK ---
# Hämta API-nyckeln automatiskt från Streamlit Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📡 DATAKÄLLA: BILD")
        bild = st.file_uploader("Ladda upp bild", type=["jpg", "png", "jpeg"])
        if bild: 
            st.image(bild, use_container_width=True)

    with col2:
        st.subheader("🧠 PROCESSOR: STIL")
        stil = st.selectbox("Välj tema:", ["Cyberpunk", "Cinematic", "Vintage 8mm", "Anime", "Dreamy Jazz"])
        rorelse = st.radio("Välj kamerarörelse:", [
            "Slow cinematic zoom in on face", 
            "Slow pan from left to right", 
            "The person is smiling and blinking",
            "Atmospheric slow motion with particles"
        ])
        
        if st.button("⚡ INITIALISERA GENERERING"):
            if not bild:
                st.error("SYSTEMFEL: Ingen bild hittades!")
            else:
                with st.status("PROSESSERAR NEON-DATA...", expanded=True):
                    try:
                        # Video & Musik (MiniMax)
                        v_url = str(replicate.run(
                            "minimax/video-01", 
                            input={"prompt": f"{rorelse}, {stil} style", "first_frame_image": bild}
                        ))
                        m_url = str(replicate.run(
                            "minimax/music-1.5", 
                            input={"prompt": f"{stil} soundtrack", "lyrics": "[Instrumental]"}
                        ))

                        # Montering
                        with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v.mp4")
                        audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                        
                        st.video("out.mp4")
                        with open("out.mp4", "rb") as f:
                            st.download_button("💾 EXPORTERA FIL", f, "ai_neon_film.mp4")
                    except Exception as e:
                        st.error(f"SYSTEMFEL: {e}")
else:
    st.error("⚠️ ÅTKOMST NEKAD: Lägg till REPLICATE_API_TOKEN i Streamlit Secrets.")







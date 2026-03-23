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
    .main { background-color: #050505; }
    .neon-wrapper {
        background-color: #0a0a0a; padding: 30px; border-radius: 15px;
        border: 1px solid #00f2ff; box-shadow: 0px 0px 20px #00f2ff;
        text-align: center; margin-bottom: 40px;
    }
    .neon-text {
        font-family: 'Courier New', Courier, monospace; font-size: 50px;
        font-weight: 900; color: #fff;
        text-shadow: 0 0 5px #fff, 0 0 20px #00f2ff; margin: 0;
    }
    .neon-sub { color: #00f2ff; letter-spacing: 5px; font-size: 12px; margin-top: 10px; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 15px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-wrapper"><p class="neon-text">TOMINGAI</p><p class="neon-sub">A.I. NEON ENGINE // FULL PRODUCTION</p></div>', unsafe_allow_html=True)

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
            # NYTT: Knapp för att låta AI:n skriva texten åt dig
            if st.button("🪄 SKAPA MAGISK TEXT"):
                with st.spinner("AI:n skriver låttext..."):
                    try:
                        # Vi låter en text-modell (Llama 3) skriva texten
                        lyrics_prompt = f"Write 4 short rhyming lines for a song. Theme: Digital future and the person in the image. Style: Poetic. Language: Swedish."
                        lyrics_ai = replicate.run(
                            "meta/meta-llama-3-70b-instruct",
                            input={"prompt": lyrics_prompt, "max_new_tokens": 100}
                        )
                        st.session_state['ai_lyrics'] = "".join(lyrics_ai)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Text-fel: {e}")

    with col2:
        st.subheader("🧠 PROCESSOR: MANUS & SÅNG")
        stil = st.selectbox("Välj musikstil:", ["Cyberpunk", "Pop", "Jazz", "Hip Hop", "Epic Orchestral"])
        
        # Här hamnar den genererade texten automatiskt
        user_lyrics = st.text_area("Låttext (Lyrics):", st.session_state.get('ai_lyrics', "[Instrumental]"))
        
        rorelse = st.radio("Kamerarörelse:", [
            "Slow cinematic zoom in on face", 
            "Slow pan from left to right", 
            "The person is smiling and blinking"
        ])
        
        if st.button("⚡ INITIALISERA FULL PRODUKTION"):
            if not bild:
                st.error("Ladda upp en bild först!")
            else:
                with st.status("PROSESSERAR NEON-DATA...", expanded=True):
                    try:
                        # 1. Skapa Video
                        st.write("🎥 Genererar video...")
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": f"{rorelse}, {stil} style", "first_frame_image": bild}))

                        # 2. Skapa Musik/Sång
                        st.write("🎵 Komponerar musik och sång...")
                        m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{stil} style, high quality", "lyrics": user_lyrics}))

                        # 3. Montering
                        st.write("✂️ Synkar ljud och bild...")
                        with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v.mp4")
                        audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                        
                        st.video("out.mp4")
                        with open("out.mp4", "rb") as f:
                            st.download_button("💾 EXPORTERA MÄSTERVERK", f, "tomingai_video.mp4")
                        
                    except Exception as e:
                        st.error(f"SYSTEMFEL: {e}")
else:
    st.error("⚠️ ÅTKOMST NEKAD: Lägg till REPLICATE_API_TOKEN i Streamlit Secrets.")







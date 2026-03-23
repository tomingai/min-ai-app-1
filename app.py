import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="AI Director Studio", page_icon="🎬", layout="wide")

# Hämta API-nyckeln automatiskt från Streamlit Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

st.title("🎬 AI Director Studio")
st.markdown("Skapa filmiska ögonblick med MiniMax AI.")

# --- 2. LOGIK ---
if api_key_found:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Ladda upp din bild")
        bild = st.file_uploader("Välj en bild", type=["jpg", "png", "jpeg"])
        if bild: 
            st.image(bild, use_container_width=True)

    with col2:
        st.subheader("2. Regissörens val")
        stil = st.selectbox("Välj stil:", ["Cinematic", "Cyberpunk", "Vintage 8mm", "Anime", "Dreamy Jazz"])
        rorelse = st.radio("Välj kamerarörelse:", [
            "Slow cinematic zoom in on face", 
            "Slow pan from left to right", 
            "The person is smiling and blinking",
            "Atmospheric slow motion with particles"
        ])
        
        if st.button("🚀 PRODUCERA FILMEN"):
            if not bild:
                st.error("Ladda upp en bild först!")
            else:
                with st.status("Producerar din film...", expanded=True):
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

                        # Montering (Auto-Edit)
                        with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v.mp4")
                        audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                        
                        st.video("out.mp4")
                        with open("out.mp4", "rb") as f:
                            st.download_button("💾 LADDA NER FILMEN", f, "min_ai_film.mp4")
                    except Exception as e:
                        st.error(f"Ett fel uppstod: {e}")
else:
    st.error("⚠️ API-nyckel saknas! Gå till Streamlit Settings -> Secrets och lägg till REPLICATE_API_TOKEN.")

st.divider()
st.caption("Byggd med MiniMax Video-01 & Music-1.5")





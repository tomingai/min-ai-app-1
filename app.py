import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

st.set_page_config(page_title="AI Director Studio", page_icon="🎬", layout="wide")
st.title("🎬 AI Director Studio")

with st.sidebar:
    st.header("⚙️ Inställningar")
    api_key = st.text_input("Replicate API-nyckel:", type="password")
    st.divider()
    stil = st.selectbox("Välj tema:", ["Cinematic", "Cyberpunk", "Vintage 8mm", "Anime", "Dreamy Jazz"])

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Ladda upp din bild")
        bild = st.file_uploader("Välj en bild på dig själv", type=["jpg", "png", "jpeg"])
        if bild: 
            st.image(bild, use_container_width=True)

    with col2:
        st.subheader("2. Regissörens val")
        # Förinställda rörelser som vi vet fungerar bra med MiniMax
        rorelse = st.radio("Välj kamerarörelse:", [
            "Slow cinematic zoom in on face", 
            "Slow pan from left to right", 
            "The person is smiling and blinking",
            "Atmospheric slow motion with particles"
        ])
        
        m_p = st.text_input("Musikstil:", f"{stil} soundtrack, high quality")
        
        if st.button("🚀 PRODUCERA FILMEN"):
            if not bild:
                st.error("Ladda upp en bild först!")
            else:
                with st.status("Producerar din film på dig själv...", expanded=True):
                    try:
                        # Video & Musik med MiniMax (våra mest stabila modeller)
                        v_url = str(replicate.run(
                            "minimax/video-01", 
                            input={"prompt": f"{rorelse}, {stil} style", "first_frame_image": bild}
                        ))
                        m_url = str(replicate.run(
                            "minimax/music-1.5", 
                            input={"prompt": m_p, "lyrics": "[Instrumental]"}
                        ))

                        # Montering
                        with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v.mp4")
                        audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                        
                        st.video("out.mp4")
                        with open("out.mp4", "rb") as f:
                            st.download_button("💾 LADDA NER FILMEN", f, "min_ai_film.mp4")
                    except Exception as e:
                        st.error(f"Produktions-fel: {e}")
else:
    st.info("Klistra in din API-nyckel i sidomenyn!")





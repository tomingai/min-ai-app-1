import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

st.set_page_config(page_title="AI Director Studio", page_icon="🎬", layout="wide")
st.title("🎬 AI Director Studio: Manus & Stil")

with st.sidebar:
    st.header("⚙️ Inställningar")
    api_key = st.text_input("Replicate API-nyckel:", type="password")
    st.divider()
    stil = st.selectbox("Välj tema:", ["Cinematic", "Cyberpunk", "Vintage 8mm", "Anime", "Horror", "Dreamy Jazz"])

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    col1, col2 = st.columns(2)
    with col1:
        bild = st.file_uploader("1. Ladda upp din bild", type=["jpg", "png", "jpeg"])
        if bild: 
            st.image(bild, use_container_width=True)
            if st.button("🪄 Skapa magiskt manus"):
                with st.spinner("AI:n analyserar din bild..."):
                    try:
                        # Vi använder moondream2 - den är blixtsnabb och stabil!
                        analysis = replicate.run(
                            "lucataco/moondream2:6108f974860f4e164223298cf085b306b3a0e6983802e3b2e04332468205f037",
                            input={"image": bild, "prompt": "Describe this person and the scene briefly for a movie script."}
                        )
                        beskrivning = "".join(analysis)
                        st.session_state['v_prompt'] = f"{beskrivning}. Cinematic camera movement, {stil} style."
                        st.session_state['m_prompt'] = f"{stil} music soundtrack, high quality"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Analys-fel: {e}")

    with col2:
        st.subheader("2. Regissörens manus")
        v_p = st.text_input("Videon ska göra:", st.session_state.get('v_prompt', "Slow zoom on face"))
        m_p = st.text_input("Musiken ska vara:", st.session_state.get('m_prompt', "Cinematic ambient"))
        
        if st.button("🚀 PRODUCERA FILMEN"):
            with st.status("Producerar din film...", expanded=True):
                try:
                    # Video & Musik med MiniMax
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": v_p, "first_frame_image": bild}))
                    m_url = str(replicate.run("minimax/music-1.5", input={"prompt": m_p, "lyrics": "[Instrumental]"}))

                    # Montering
                    with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    
                    clip = VideoFileClip("v.mp4")
                    audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                    
                    st.video("out.mp4")
                    with open("out.mp4", "rb") as f:
                        st.download_button("💾 LADDA NER", f, "ai_video.mp4")
                except Exception as e:
                    st.error(f"Produktions-fel: {e}")
else:
    st.info("Klistra in din API-nyckel i sidomenyn!")




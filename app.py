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
    st.subheader("🎨 Välj Filmstil")
    stil = st.selectbox("Välj tema:", ["Cinematic", "Cyberpunk", "Vintage 8mm", "Anime", "Horror", "Dreamy Jazz"])

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    col1, col2 = st.columns(2)
    with col1:
        bild = st.file_uploader("1. Ladda upp din startbild", type=["jpg", "png", "jpeg"])
        if bild: 
            st.image(bild, use_container_width=True)
            if st.button("🪄 Skapa magiskt manus från bilden"):
                with st.spinner("AI:n analyserar bilden..."):
                    # Vi använder Llava för att beskriva bilden och skapa en prompt
                    analysis = replicate.run(
                        "yorickvp/llava-13b:b5f6223d27a765353842d76c374668f1c8411c97a552554a9d7b97e930f30501",
                        input={"image": bild, "prompt": f"Describe a cinematic camera movement for this image in {stil} style. Keep it under 20 words."}
                    )
                    st.session_state['v_prompt'] = "".join(analysis)
                    st.session_state['m_prompt'] = f"{stil} music soundtrack, high quality"

    with col2:
        st.subheader("2. Regissörens manus")
        v_prompt = st.text_input("Videon ska göra:", st.session_state.get('v_prompt', "Slow camera zoom"))
        m_prompt = st.text_input("Musiken ska vara:", st.session_state.get('m_prompt', "Cinematic ambient"))
        
        btn = st.button("🚀 PRODUCERA FILMEN")

    if btn and bild:
        with st.status("Producerar din film...", expanded=True):
            try:
                # 1. Generera material
                st.write("🎥 Skapar video...")
                video_url = str(replicate.run("minimax/video-01", input={"prompt": f"{v_prompt} in {stil} style", "first_frame_image": bild}))
                
                st.write("🎵 Skapar musik...")
                music_url = str(replicate.run("minimax/music-1.5", input={"prompt": m_prompt, "lyrics": "[Instrumental]"}))

                # 2. Montering (Auto-Edit)
                st.write("📥 Laddar ner och klipper...")
                with open("temp_v.mp4", "wb") as f: f.write(requests.get(video_url).content)
                with open("temp_a.mp3", "wb") as f: f.write(requests.get(music_url).content)
                
                video_clip = VideoFileClip("temp_v.mp4")
                audio_clip = AudioFileClip("temp_a.mp3").set_duration(video_clip.duration)
                final_clip = video_clip.set_audio(audio_clip)
                final_clip.write_videofile("final.mp4", codec="libx264", audio_codec="aac", remove_temp=True)
                
                st.video("final.mp4")
                with open("final.mp4", "rb") as f:
                    st.download_button("💾 LADDA NER FILMEN", data=f, file_name=f"ai_film_{stil}.mp4")

            except Exception as e:
                st.error(f"Ett fel uppstod: {e}")
else:
    st.info("Klistra in din API-nyckel i sidomenyn!")




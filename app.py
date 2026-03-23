import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

st.set_page_config(page_title="AI Studio: Auto-Editor", page_icon="🎬", layout="wide")
st.title("🎬 AI Studio: Video & Musik-mixer")

with st.sidebar:
    st.header("⚙️ Inställningar")
    api_key = st.text_input("Replicate API-nyckel:", type="password")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    col1, col2 = st.columns(2)
    with col1:
        bild = st.file_uploader("Ladda upp bild", type=["jpg", "png", "jpeg"])
        if bild: st.image(bild, use_container_width=True)

    with col2:
        v_prompt = st.text_input("Rörelse i videon:", "Cinematic slow motion")
        m_prompt = st.text_input("Musikstil:", "Epic cinematic soundtrack")
        btn = st.button("🚀 SKAPA FILMEN")

    if btn and bild:
        with st.status("Skapar och klipper ihop din film...", expanded=True) as status:
            try:
                # 1. Skapa Video och Musik
                st.write("🎥 Genererar video (MiniMax)...")
                video_url = str(replicate.run("minimax/video-01", input={"prompt": v_prompt, "first_frame_image": bild}))
                
                st.write("🎵 Genererar musik (MiniMax)...")
                music_url = str(replicate.run("minimax/music-1.5", input={"prompt": m_prompt, "lyrics": "[Instrumental]"}))

                # 2. Ladda ner filerna till Streamlits server
                st.write("📥 Laddar ner filer för redigering...")
                with open("temp_v.mp4", "wb") as f: f.write(requests.get(video_url).content)
                with open("temp_a.mp3", "wb") as f: f.write(requests.get(music_url).content)
                
                # 3. Montera (Auto-Edit)
                st.write("✂️ Monterar ljud på bild...")
                video_clip = VideoFileClip("temp_v.mp4")
                audio_clip = AudioFileClip("temp_a.mp3").set_duration(video_clip.duration)
                
                final_clip = video_clip.set_audio(audio_clip)
                final_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
                
                # 4. Visa och Ladda ner
                st.video("final_video.mp4")
                
                with open("final_video.mp4", "rb") as f:
                    st.download_button("💾 LADDA NER DIN FÄRDIGA FILM", data=f, file_name="ai_film_med_ljud.mp4", mime="video/mp4")
                
                # Städa upp
                video_clip.close()
                audio_clip.close()
                
                st.success("Mästerverket är klart!")

            except Exception as e:
                st.error(f"Ett fel uppstod vid monteringen: {e}")
else:
    st.info("Klistra in din API-nyckel i sidomenyn!")




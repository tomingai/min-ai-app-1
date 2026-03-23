import streamlit as st
import replicate
import os
import requests

st.set_page_config(page_title="AI Studio: Final Cut", page_icon="🎬", layout="wide")

st.title("🎬 AI Studio: Video & Musik")

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
        btn = st.button("🚀 SKAPA")

    if btn and bild:
        with st.status("AI:n jobbar...", expanded=True):
            try:
                # 1. Skapa Video
                st.write("🎥 Skapar video med MiniMax...")
                video_res = replicate.run(
                    "minimax/video-01", 
                    input={"prompt": v_prompt, "first_frame_image": bild}
                )
                
                # 2. Skapa Musik
                st.write("🎵 Skapar musik...")
                music_res = replicate.run(
                    "minimax/music-1.5", 
                    input={"prompt": m_prompt, "lyrics": "[Instrumental]"}
                )

                # Visa resultaten direkt (säkraste sättet)
                st.subheader("Ditt resultat")
                st.video(str(video_res))
                st.audio(str(music_res))
                
                st.success("Klart! Du kan nu spara filerna var för sig.")

            except Exception as e:
                st.error(f"Ett fel uppstod: {e}")
else:
    st.info("Klistra in din API-nyckel i sidomenyn!")




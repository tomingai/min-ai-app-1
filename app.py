import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Multi-Studio 2026", layout="centered")
st.title("🎬 AI Studio: Bild ➔ Video ➔ Musik")

with st.sidebar:
    st.header("Inställningar")
    api_key = st.text_input("Klistra in din Replicate API-nyckel:", type="password")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    bild = st.file_uploader("Ladda upp en bild", type=["jpg", "png", "jpeg"])
    
    if bild:
        st.image(bild, caption="Din bild", use_container_width=True)
        if st.button("🚀 Starta generering"):
            
            # --- STEG 1: SKAPA VIDEO ---
            with st.spinner("Skapar video... (ca 60 sekunder)"):
                try:
                    # Senaste stabila versionen för Stable Video Diffusion
                    video_output = replicate.run(
                        "stability-ai/stable-video-diffusion:ac7327c2014dba223a6ca27c770315e794961d552e751fd3f23019705537e83e",
                        input={"input_image": bild}
                    )
                    st.subheader("1. Din AI-Video")
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Kunde inte skapa video: {e}")

            # --- STEG 2: SKAPA MUSIK ---
            with st.spinner("Skapar matchande musik..."):
                try:
                    # Senaste stabila versionen för MusicGen
                    music_output = replicate.run(
                        "facebookresearch/musicgen:7b3212fb7983471439735c0529d06634",
                        input={"prompt": "cinematic soundtrack, high quality, melodic", "duration": 8}
                    )
                    st.subheader("2. Din AI-Musik")
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Kunde inte skapa musik: {e}")
            
            st.success("✨ Generering slutförd!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")


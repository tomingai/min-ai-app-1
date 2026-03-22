import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Studio Pro", layout="centered")
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
            
            # --- 1. VIDEO (Stability AI - SVD-XT senaste stabila version) ---
            with st.spinner("Animerar bild... (ca 1 min)"):
                try:
                    video_output = replicate.run(
                        "stability-ai/stable-video-diffusion:ac7327c2014dba223a6ca27c770315e794961d552e751fd3f23019705537e83e",
                        input={"input_image": bild}
                    )
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. MUSIK (MusicGen Melody - Senaste stabila version) ---
            with st.spinner("Komponerar musik..."):
                try:
                    music_output = replicate.run(
                        "facebookresearch/musicgen:7b3212fb7983471439735c0529d06634",
                        input={"prompt": "cinematic and emotional soundtrack", "duration": 8}
                    )
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Generering klar!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")




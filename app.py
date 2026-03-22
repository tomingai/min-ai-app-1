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
            
            # --- 1. SKAPA VIDEO (Universalversion) ---
            with st.spinner("Animerar bild... (ca 1 min)"):
                try:
                    # Vi tar bort sifferkoden och låter Replicate välja den senaste automatiskt
                    # Om det blir 404, byter vi till en annan modell i nästa steg
                    video_output = replicate.run(
                        "stability-ai/stable-video-diffusion",
                        input={"input_image": bild}
                    )
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. SKAPA MUSIK (Universalversion) ---
            with st.spinner("Komponerar musik..."):
                try:
                    # Samma här, vi använder bara huvudnamnet
                    music_output = replicate.run(
                        "facebookresearch/musicgen",
                        input={"prompt": "cinematic and emotional soundtrack", "duration": 8}
                    )
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Generering klar!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")


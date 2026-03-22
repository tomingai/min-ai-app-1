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
            
            # --- 1. SKAPA VIDEO (Senaste SVD) ---
            with st.spinner("Animerar bild... (ca 1 min)"):
                try:
                    # Vi tar bort sifferkoden efter kolonet för att få senaste versionen
                    model = replicate.models.get("stability-ai/stable-video-diffusion")
                    version = model.versions.list()[0] # Hämtar den nyaste versionen automatiskt
                    video_output = version.predict(input_image=bild)
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. SKAPA MUSIK (Senaste MusicGen) ---
            with st.spinner("Komponerar musik..."):
                try:
                    # Samma här, hämtar senaste versionen automatiskt
                    model = replicate.models.get("facebookresearch/musicgen")
                    version = model.versions.list()[0]
                    music_output = version.predict(prompt="cinematic soundtrack", duration=8)
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Generering klar!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")



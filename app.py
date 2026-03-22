import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Studio Pro", layout="centered")
st.title("🎬 AI Studio: Bild ➔ Video ➔ Musik")

with st.sidebar:
    api_key = st.text_input("Klistra in din Replicate API-nyckel:", type="password")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    bild = st.file_uploader("Ladda upp en bild", type=["jpg", "png", "jpeg"])
    
    if bild:
        st.image(bild, caption="Din bild", use_container_width=True)
        if st.button("🚀 Starta generering"):
            
            # --- 1. SKAPA VIDEO (Luma Dream Machine - Mycket stabilare!) ---
            with st.spinner("Animerar bild... (ca 1-2 min)"):
                try:
                    # Vi använder den senaste Luma-modellen
                    video_output = replicate.run(
                        "lumalabs/dream-machine",
                        input={"prompt": "animate this image", "image_url": bild}
                    )
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. SKAPA MUSIK (MusicGen - Senaste versionen) ---
            with st.spinner("Komponerar musik..."):
                try:
                    music_output = replicate.run(
                        "facebookresearch/musicgen",
                        input={"prompt": "cinematic soundtrack", "duration": 8}
                    )
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Generering klar!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")



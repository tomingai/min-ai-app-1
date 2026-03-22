import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Studio 2.0", layout="centered")
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
            with st.spinner("AI:n animerar din bild... (ca 1 min)"):
                try:
                    # Vi använder modellnamnet utan sifferkod för att få senaste versionen
                    video_output = replicate.run(
                        "stability-ai/stable-video-diffusion",
                        input={"input_image": bild}
                    )
                    st.subheader("1. Din AI-Video")
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- STEG 2: SKAPA MUSIK ---
            with st.spinner("AI:n komponerar musik..."):
                try:
                    # Vi använder modellnamnet utan sifferkod här också
                    music_output = replicate.run(
                        "facebookresearch/musicgen",
                        input={"prompt": "cinematic and emotional soundtrack", "duration": 8}
                    )
                    st.subheader("2. Din AI-Musik")
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Allt klart!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")


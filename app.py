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
            
            # --- 1. SKAPA VIDEO (Ny stabil modell: Luma Dream Machine eller SVD-XT) ---
            with st.spinner("Animerar bild... (ca 1 min)"):
                try:
                    # Vi använder den senaste versionen av SVD via en förenklad länk
                    video_output = replicate.run(
                        "stability-ai/stable-video-diffusion:ac7327c2014dba223a6ca27c770315e794961d552e751fd3f23019705537e83e",
                        input={"input_image": bild}
                    )
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. SKAPA MUSIK (Ny stabil modell: AudioLDM) ---
            with st.spinner("Komponerar musik..."):
                try:
                    # Vi byter till AudioLDM som ofta är mer tillåtande
                    music_output = replicate.run(
                        "cvssp/audioldm:b61392adec474775060c0ad3f71bc5a951458a5c97818b4e551f8aba3969139d",
                        input={"text": "cinematic and emotional soundtrack", "duration": "10"}
                    )
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Generering klar!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")



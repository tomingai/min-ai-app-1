import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Multi-Studio", layout="centered")
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
            with st.spinner("AI:n jobbar... vänta ca 1 min."):
                try:
                    # Skapa Video (Uppdaterad version)
                    vid = replicate.run(
                        "stability-ai/stable-video-diffusion", 
                        input={"input_image": bild}
                    )
                    st.video(vid)
                    
                    # Skapa Musik
                    mus = replicate.run(
                        "facebookresearch/musicgen", 
                        input={"prompt": "cinematic music", "duration": 8}
                    )
                    st.audio(mus)
                    st.success("Klart!")
                except Exception as e:
                    st.error(f"Ett fel uppstod: {e}")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")


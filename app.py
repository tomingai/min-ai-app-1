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
        if st.button("🚀 Skapa Video & Musik"):
            with st.spinner("AI:n jobbar... vänta ca 1 min."):
                # Skapa Video
                vid = replicate.run("stability-ai/stable-video-diffusion:ac7327c2014dba223a6ca27c770315e794961d552e751fd3f23019705537e83e", input={"input_image": bild})
                st.video(vid)
                # Skapa Musik
                mus = replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": "cinematic music", "duration": 8})
                st.audio(mus)
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")

import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Studio", layout="centered")
st.title("🎬 AI Studio: Bild ➔ Video ➔ Musik")

with st.sidebar:
    api_key = st.text_input("Klistra in din Replicate API-nyckel:", type="password")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    bild = st.file_uploader("Ladda upp en bild", type=["jpg", "png", "jpeg"])
    
    if bild:
        st.image(bild, caption="Din bild", use_container_width=True)
        if st.button("🚀 Starta generering"):
            with st.spinner("AI:n jobbar... vänta ca 1-2 minuter."):
                try:
                    # 1. Skapa Video (Senaste stabila versionen av SVD-XT)
                    vid = replicate.run(
                        "stability-ai/stable-video-diffusion:3f0ad1d533866c105be60ca8cd20f7efba29a1a45749f3e098863f6a27e3d166",
                        input={"input_image": bild, "video_length": "14_frames_with_svd"}
                    )
                    st.video(vid)
                    
                    # 2. Skapa Musik (Senaste versionen av MusicGen Melody)
                    mus = replicate.run(
                        "facebookresearch/musicgen:7b3212fb7983471439735c0529d06634",
                        input={"prompt": "cinematic and atmospheric music", "duration": 8}
                    )
                    st.audio(mus)
                    st.success("Klart!")
                except Exception as e:
                    st.error(f"Ett fel uppstod: {e}")
                    st.info("Tips: Kontrollera att du har lagt in ett betalkort på Replicate (billing) då gratis-testningen ofta är begränsad.")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")



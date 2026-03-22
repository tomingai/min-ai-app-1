import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Studio Pro: MiniMax", layout="centered")
st.title("🎬 AI Studio: Bild ➔ Video ➔ Musik")

with st.sidebar:
    st.header("Inställningar")
    api_key = st.sidebar.text_input("Klistra in din Replicate API-nyckel:", type="password")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    bild = st.file_uploader("Ladda upp en bild", type=["jpg", "png", "jpeg"])
    
    if bild:
        st.image(bild, caption="Din bild", use_container_width=True)
        prompt_text = st.text_input("Beskriv rörelsen:", "cinematic movement, high quality")
        
        if st.button("🚀 Starta AI-generering"):
            
            # --- 1. SKAPA VIDEO (MiniMax) ---
            with st.spinner("MiniMax skapar video... (ca 1-2 min)"):
                try:
                    video_output = replicate.run(
                        "minimax/video-01",
                        input={
                            "prompt": prompt_text,
                            "first_frame_image": bild,
                            "prompt_optimizer": True
                        }
                    )
                    st.subheader("1. Din AI-Video")
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. SKAPA MUSIK (AudioLDM - Stabilare!) ---
            with st.spinner("Komponerar musik..."):
                try:
                    # Vi använder AudioLDM som är mycket mer pålitlig för API:er
                    music_output = replicate.run(
                        "cvssp/audioldm:b61392adec474775060c0ad3f71bc5a951458a5c97818b4e551f8aba3969139d",
                        input={
                            "text": f"cinematic soundtrack for {prompt_text}",
                            "duration": "10"
                        }
                    )
                    st.subheader("2. Din AI-Musik")
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Allt klart!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")



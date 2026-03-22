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
            
            # --- 1. SKAPA VIDEO (Pika - Mycket stabil modell) ---
            with st.spinner("Animerar bild... (ca 1 min)"):
                try:
                    # Vi använder den senaste stabila Pika-modellen
                    video_output = replicate.run(
                        "pika/pika-art:63606a246874a90f96894c25d80429f582f3b9e4368132e05b9b8b0e7d56e9c9",
                        input={"image": bild}
                    )
                    st.video(video_output)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. SKAPA MUSIK (AudioLDM - Mycket stabil modell) ---
            with st.spinner("Komponerar musik..."):
                try:
                    # Vi använder AudioLDM som är känd för att fungera direkt
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




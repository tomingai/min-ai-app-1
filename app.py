import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Studio Pro: MiniMax", layout="centered")
st.title("🎬 AI Studio: Bild ➔ Video (MiniMax) ➔ Musik")

with st.sidebar:
    st.header("Inställningar")
    api_key = st.text_input("Klistra in din Replicate API-nyckel:", type="password")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    bild = st.file_uploader("Ladda upp en bild", type=["jpg", "png", "jpeg"])
    
    if bild:
        st.image(bild, caption="Din bild", use_container_width=True)
        prompt_text = st.text_input("Beskriv rörelsen:", "cinematic movement, high quality")
        
        if st.button("🚀 Starta MiniMax-generering"):
            
            # --- 1. SKAPA VIDEO (MiniMax Video-01) ---
            with st.spinner("MiniMax skapar video... (ca 1-2 min)"):
                try:
                    output = replicate.run(
                        "minimax/video-01",
                        input={
                            "prompt": prompt_text,
                            "first_frame_image": bild,
                            "prompt_optimizer": True
                        }
                    )
                    # FIX: Vi använder .url för att Streamlit ska kunna visa videon rätt
                    st.subheader("Din AI-Video")
                    st.video(output.url)
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. SKAPA MUSIK (MusicGen) ---
            with st.spinner("Komponerar musik..."):
                try:
                    # Uppdaterad sifferkod för MusicGen Melody
                    music_output = replicate.run(
                        "facebookresearch/musicgen:7b3212fb7983471439735c0529d06634",
                        input={"prompt": f"soundtrack for {prompt_text}", "duration": 10}
                    )
                    st.subheader("Din AI-Musik")
                    # Musik-AI returnerar också en länk som vi spelar upp
                    st.audio(music_output)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Allt klart!")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")



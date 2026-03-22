import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Studio: MiniMax Pro", layout="centered")
st.title("🎬 AI Studio: MiniMax Video & Musik")

with st.sidebar:
    st.header("Inställningar")
    api_key = st.sidebar.text_input("Klistra in din Replicate API-nyckel:", type="password")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    bild = st.file_uploader("Ladda upp en bild (för videon)", type=["jpg", "png", "jpeg"])
    
    if bild:
        st.image(bild, caption="Din bild", use_container_width=True)
        
        # Inmatning för video-rörelse och låttext
        v_prompt = st.text_input("Vad ska hända i videon?", "Cinematic slow motion")
        lyrics = st.text_area("Skriv din låttext här (Lyrics):", "[Verse]\nStjärnorna lyser över staden ikväll,\nVi bygger en värld, en digital säll.")
        m_prompt = st.text_input("Musikstil (t.ex. Pop, Jazz, Rock):", "Pop, Melodic, High Quality")
        
        if st.button("🚀 Starta Full AI-Generering"):
            
            # --- 1. SKAPA VIDEO (MiniMax Video-01) ---
            with st.spinner("MiniMax skapar video... (ca 1-2 min)"):
                try:
                    video_result = replicate.run(
                        "minimax/video-01",
                        input={
                            "prompt": v_prompt,
                            "first_frame_image": bild,
                            "prompt_optimizer": True
                        }
                    )
                    st.subheader("1. Din AI-Video")
                    st.video(str(video_result))
                except Exception as e:
                    st.error(f"Video-fel: {e}")

            # --- 2. SKAPA MUSIK (MiniMax Music-1.5) ---
            with st.spinner("MiniMax skapar musik med sång..."):
                try:
                    music_result = replicate.run(
                        "minimax/music-1.5",
                        input={
                            "lyrics": lyrics,
                            "prompt": m_prompt,
                            "audio_format": "mp3"
                        }
                    )
                    st.subheader("2. Din AI-Musik")
                    # Vi använder .url för att spela upp MiniMax musik direkt
                    st.audio(music_result.url)
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
            
            st.success("✨ Allt klart! Din musikvideo är redo.")
else:
    st.info("Börja med att klistra in din API-nyckel i sidomenyn!")




import streamlit as st
import replicate
import os

# Inställningar för sidan
st.set_page_config(page_title="AI Multi-Studio", page_icon="🎬", layout="centered")

st.title("🎬 AI Studio: Bild ➔ Video ➔ Musik")
st.markdown("Skapa magi genom att ladda upp en enda bild.")

# Sidomeny för API-nyckel
with st.sidebar:
    st.header("Inställningar")
    api_key = st.text_input("Klistra in din Replicate API-nyckel:", type="password")
    st.info("Hämta din nyckel på ://replicate.com")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    # Filuppladdare
    uploaded_file = st.file_uploader("Välj en bild (JPG eller PNG)", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Din valda bild", use_container_width=True)
        
        if st.button("🚀 Starta generering"):
            col1, col2 = st.columns(2)
            
            # 1. Skapa Video
            with col1:
                st.subheader("1. Skapar Video...")
                video_placeholder = st.empty()
                with st.spinner("Animerar bilden..."):
                    video_output = replicate.run(
                        "stability-ai/stable-video-diffusion:ac7327c2014dba223a6ca27c770315e794961d552e751fd3f23019705537e83e",
                        input={"input_image": uploaded_file, "video_length": "14_frames_with_svd"}
                    )
                    video_placeholder.video(video_output)
            
            # 2. Skapa Musik
            with col2:
                st.subheader("2. Skapar Musik...")
                audio_placeholder = st.empty()
                with st.spinner("Komponerar soundtrack..."):
                    # Vi ber MusicGen skapa något episkt som passar en video
                    music_output = replicate.run(
                        "facebookresearch/musicgen:7b3212fb7983471439735c0529d06634",
                        input={
                            "prompt": "Cinematic soundtrack, high quality, matching the mood of the uploaded visual",
                            "duration": 10
                        }
                    )
                    audio_placeholder.audio(music_output)
            
            st.success("✨ Allt klart! Du har skapat en video och musik från en bild.")
else:
    st.warning("👈 Du måste klistra in din API-nyckel i sidomenyn för att appen ska fungera.")

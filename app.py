import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="TOMINGAI NEON STUDIO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    .neon-container {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
        padding: 40px; border-radius: 20px; border: 2px solid #00f2ff;
        box-shadow: 0px 0px 40px rgba(0, 242, 255, 0.4);
        text-align: center; margin-bottom: 50px;
    }
    .neon-title {
        font-family: 'Arial Black', sans-serif; font-size: 75px; font-weight: 900;
        color: #ffffff; text-transform: uppercase; letter-spacing: 10px;
        text-shadow: 0 0 10px #fff, 0 0 40px #00f2ff, 0 0 80px #00f2ff;
    }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px;">A.I. MAGIC VISION STUDIO</p></div>', unsafe_allow_html=True)

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    st.subheader("🎵 SKAPA VIDEO & MUSIK FRÅN EN ENDA RAD")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_input = st.text_input("Skriv din låtrad eller känsla (t.ex. 'Ensam varg i neonljus'):", "En natt i framtiden")
        stil = st.selectbox("Välj visuell stil:", ["Cyberpunk", "Cinematic Photo", "Digital Art", "Anime"])
        rost = st.radio("Sångröst:", ["Kvinna", "Man"], horizontal=True)

    if st.button("🚀 SKAPA ALLT (BILD + MUSIK + VIDEO)"):
        with st.status("AI-hjärnan bearbetar din idé...", expanded=True) as status:
            try:
                # 1. Skriv låttexten (Llama)
                st.write("📝 Skriver låttext på svenska...")
                lyrics_res = replicate.run("meta/meta-llama-3-70b-instruct", 
                    input={"prompt": f"Skriv 4 korta rimmade rader på svenska om: {user_input}."})
                final_lyrics = "".join(lyrics_res).replace('"', '')
                
                # 2. Skapa matchande bild (FLUX)
                st.write("🎨 Ritar en matchande bild...")
                image_res = replicate.run(
                    "black-forest-labs/flux-schnell",
                    input={"prompt": f"A high quality {stil} image representing: {user_input}. 4k, cinematic lighting.", "aspect_ratio": "16:9"}
                )
                image_url = image_res[0]
                st.image(image_url, caption="AI-genererad bakgrund")

                # 3. Skapa Video (MiniMax)
                st.write("🎥 Animerar bilden...")
                video_url = str(replicate.run("minimax/video-01", 
                    input={"prompt": "Cinematic movement, slow motion", "first_frame_image": image_url}))

                # 4. Skapa Musik (MiniMax)
                st.write("🎵 Komponerar sången...")
                music_url = str(replicate.run("minimax/music-1.5", 
                    input={"prompt": f"{stil} music, {rost} vocals", "lyrics": final_lyrics}))

                # 5. Montering (Mixer)
                st.write("✂️ Klipper ihop allt...")
                with open("v.mp4", "wb") as f: f.write(requests.get(video_url).content)
                with open("a.mp3", "wb") as f: f.write(requests.get(music_url).content)
                
                clip = VideoFileClip("v.mp4")
                audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                clip.set_audio(audio).write_videofile("final.mp4", codec="libx264", audio_codec="aac")
                
                st.video("final.mp4")
                st.success(f"Sångtext: {final_lyrics}")
                st.download_button("💾 LADDA NER DIN AI-FILM", open("final.mp4", "rb"), "tomingai_magic.mp4")

            except Exception as e:
                st.error(f"Ett fel uppstod: {e}")
else:
    st.error("Nyckel saknas i Secrets!")








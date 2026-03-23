import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- DESIGN & SETUP ---
st.set_page_config(page_title="TOMINGAI MUSIC STUDIO", page_icon="🎵", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stSlider > div > div > div > div { background: #00f2ff; }
    .neon-title { color: #fff; text-shadow: 0 0 20px #00f2ff; font-size: 40px; font-weight: 900; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="neon-title">🎵 TOMINGAI MUSIC & VIDEO STUDIO</p>', unsafe_allow_html=True)

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 VISUELL KÄLLA")
        bild = st.file_uploader("Ladda upp bild", type=["jpg", "png", "jpeg"])
        if bild: st.image(bild, use_container_width=True)
        
        st.divider()
        st.subheader("🎬 KAMERAREGISSÖR")
        v_prompt = st.text_area("Beskriv rörelsen:", "Cinematic slow motion, high quality")

    with col2:
        st.subheader("🎸 MUSIKPRODUCENT")
        # Här skapar vi din egen musik-mixer!
        genre = st.selectbox("Huvudgenre:", ["Synthwave", "Heavy Metal", "Deep House", "Acoustic Guitar", "Lofi Hip Hop", "Swedish Pop"])
        mood = st.select_slider("Stämning:", options=["Mörkt/Dramatiskt", "Lugnt", "Energiskt", "Glatt"])
        
        instrument = st.text_input("Extra instrument (t.ex. 'Saxofon', 'Distad elgitarr'):", "Synthesizer")
        
        # Sång-sektionen
        lyrics = st.text_area("Låttext (Lämna tom för instrumental):", "[Instrumental]")
        rost = st.radio("Sångröst:", ["Kvinna", "Man"])

        # Bygg ihop musik-prompten automatiskt
        final_m_prompt = f"{genre}, {mood}, featuring {instrument}, high quality studio recording"

        if st.button("🚀 PRODUCERA MÄSTERVERK"):
            if not bild:
                st.error("Ladda upp en bild först!")
            else:
                with st.status("Skapar din unika musik och video...", expanded=True):
                    try:
                        # 1. Generera Video
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": v_prompt, "first_frame_image": bild}))
                        
                        # 2. Generera Egen Musik
                        st.write(f"🎵 Komponerar: {final_m_prompt}...")
                        m_url = str(replicate.run("minimax/music-1.5", input={
                            "prompt": final_m_prompt,
                            "lyrics": lyrics,
                            "audio_format": "mp3"
                        }))

                        # 3. Montering
                        with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v.mp4")
                        audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                        
                        st.video("out.mp4")
                        st.download_button("💾 LADDA NER FILMEN", open("out.mp4", "rb"), "tomingai_studio.mp4")
                    except Exception as e:
                        st.error(f"Fel: {e}")
else:
    st.error("Nyckel saknas i Secrets!")







import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="TOMINGAI MEGA STUDIO", page_icon="⚡", layout="wide")

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
        font-family: 'Arial Black', sans-serif; font-size: 60px; font-weight: 900;
        color: #ffffff; text-transform: uppercase; letter-spacing: 5px;
        text-shadow: 0 0 10px #fff, 0 0 40px #00f2ff;
    }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px;">MEGA AI ENGINE // ALL FEATURES</p></div>', unsafe_allow_html=True)

# --- SIDOMENY: SPRÅK & GLOBAL SETTINGS ---
with st.sidebar:
    st.header("🌐 Språk-Motor")
    input_lang = st.selectbox("Jag skriver på:", ["Svenska", "English", "Español", "Français", "日本語", "Deutsch"])
    output_lang = st.selectbox("AI:n ska sjunga på:", ["English", "Svenska", "Español", "Français", "日本語", "Italiano"])
    st.divider()
    st.header("🎤 Sånginställning")
    magic_rost = st.radio("Sångröst:", ["Kvinna", "Man"])
    st.divider()
    st.info(f"Studio Tomingai översätter {input_lang} ➔ {output_lang}")

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    # ÅTERINFÖR FLIKARNA SÅ DU KAN VÄLJA METOD
    tab1, tab2 = st.tabs(["🪄 TOTAL MAGI (AI RITAR)", "🎬 REGISSÖREN (DU LADDAR UPP)"])

    # --- FLIK 1: TOTAL MAGI ---
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            magic_ide = st.text_area(f"Din idé på {input_lang}:", f"En vacker natt i Tokyo", key="m_ide")
            magic_stil = st.selectbox("Filmstil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Anime"], key="m_stil")
        with col2:
            st.write("AI:n kommer rita en bild, skriva text och skapa video automatiskt.")
            if st.button("🚀 SKAPA MAGI", key="m_btn"):
                with st.status("Producerar...") as status:
                    # 1. Bild
                    img = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{magic_ide}, {magic_stil} style", "aspect_ratio": "16:9"})
                    st.image(img)
                    # 2. Text/Översättning
                    lyrics = "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Write 4 short rhyming lines in {output_lang} about '{magic_ide}'. ONLY lyrics."})).replace('"', '')
                    # 3. Video & Musik
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img}))
                    m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{magic_stil} style, {magic_rost} vocals", "lyrics": lyrics}))
                    # 4. Mix
                    with open("v1.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a1.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v1.mp4")
                    audio = AudioFileClip("a1.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out1.mp4", codec="libx264", audio_codec="aac")
                    st.video("out1.mp4")
                    st.success(f"Lyrics ({output_lang}): {lyrics}")

    # --- FLIK 2: REGISSÖREN ---
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            bild = st.file_uploader("Ladda upp egen bild", type=["jpg", "png", "jpeg"], key="r_img")
            if bild: st.image(bild, use_container_width=True)
        with col2:
            r_ide = st.text_input(f"Vad ska låten handla om? ({input_lang})", "En sång om mig själv", key="r_ide")
            r_stil = st.selectbox("Filmstil:", ["Cyberpunk", "Cinematic", "Anime"], key="r_stil")
            if st.button("⚡ PRODUCERA", key="r_btn"):
                if bild:
                    with st.status("Jobbar..."):
                        # Samma logik som ovan fast med din bild
                        lyrics = "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Write 4 rhyming lines in {output_lang} about '{r_ide}'. ONLY lyrics."})).replace('"', '')
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": bild}))
                        m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{r_stil} style, {magic_rost} vocals", "lyrics": lyrics}))
                        # Mix...
                        with open("v2.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a2.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        clip = VideoFileClip("v2.mp4")
                        audio = AudioFileClip("a2.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out2.mp4", codec="libx264", audio_codec="aac")
                        st.video("out2.mp4")
                        st.success(f"Lyrics ({output_lang}): {lyrics}")
                else: st.error("Ladda upp en bild!")

else:
    st.error("Nyckel saknas i Secrets!")








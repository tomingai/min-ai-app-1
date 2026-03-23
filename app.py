import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="TOMINGAI WORLD STUDIO", page_icon="🌍", layout="wide")

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
        font-family: 'Arial Black', sans-serif; font-size: 70px; font-weight: 900;
        color: #ffffff; text-transform: uppercase; letter-spacing: 10px;
        text-shadow: 0 0 10px #fff, 0 0 40px #00f2ff, 0 0 80px #00f2ff;
    }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px;">WORLD AI ENGINE</p></div>', unsafe_allow_html=True)

# --- SIDOMENY: SPRÅKVAL ---
with st.sidebar:
    st.header("🌍 Global Settings")
    sprak = st.selectbox("Välj språk för låttext:", ["Svenska", "English", "Español", "Français", "Deutsch", "Italiano"])
    st.divider()
    st.info(f"AI-hjärnan kommer nu skriva på {sprak}.")

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 MUSIKSTUDION"])

    # --- FLIK 1: TOTAL MAGI (MED SPRÅKSTÖD) ---
    with tab1:
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            magic_input = st.text_input("Beskrivning:", "A neon cyber city", key="m_in")
            magic_stil = st.selectbox("Stil:", ["Cyberpunk", "Cinematic", "Anime"], key="m_stil")
        with m_col2:
            magic_rost = st.radio("Röst:", ["Kvinna", "Man"], horizontal=True, key="m_voice")
        
        if st.button("🚀 SKAPA MAGI", key="m_btn"):
            with st.status(f"Skapar allt på {sprak}...") as status:
                try:
                    img_res = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{magic_input}, {magic_stil} style", "aspect_ratio": "16:9"})
                    st.image(img_res, caption="AI Image")
                    
                    # HÄR ANVÄNDS SPRÅKVALET
                    lyrics_res = replicate.run("meta/meta-llama-3-70b-instruct", 
                        input={"prompt": f"Write 4 short rhyming lines in {sprak} about: {magic_input}. ONLY return the lyrics."})
                    final_lyr = "".join(lyrics_res).replace('"', '')

                    v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic motion", "first_frame_image": img_res}))
                    m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{magic_stil} style, {magic_rost} vocals", "lyrics": final_lyr}))

                    with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v.mp4")
                    audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                    st.video("out.mp4")
                    st.success(f"Lyrics ({sprak}): {final_lyr}")
                except Exception as e: st.error(f"Fel: {e}")

    # --- BEHÅLL ÖVRIGA FLIKAR ---
    with tab2: st.info("Använd 'Regissören' för egna bilder.")
    with tab3: st.info("Använd 'Musikstudion' för singlar.")

else:
    st.error("Nyckel saknas i Secrets!")








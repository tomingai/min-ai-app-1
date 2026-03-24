import streamlit as st
import replicate
import os
import requests
import time
from moviepy.editor import VideoFileClip, AudioFileClip, vfx

# --- 1. SETUP & DESIGN (ANIMERAD NEON-BAKGRUND) ---
st.set_page_config(page_title="TOMINGAI MEGA STUDIO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Animerad mörk gradient-bakgrund */
    .stApp {
        background: linear-gradient(125deg, #050505, #0a0a0a, #00151a, #050505);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #fff;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glas-effekt behållare */
    .neon-container {
        background: rgba(10, 10, 10, 0.85);
        padding: 50px; border-radius: 30px; 
        border: 1px solid rgba(0, 242, 255, 0.4);
        box-shadow: 0px 0px 60px rgba(0, 242, 255, 0.2);
        text-align: center; margin-bottom: 40px;
        backdrop-filter: blur(15px);
    }
    .neon-title { 
        font-family: 'Arial Black', sans-serif; font-size: 75px; font-weight: 900; 
        color: #fff; text-shadow: 0 0 10px #00f2ff, 0 0 30px #00f2ff; margin: 0; 
    }
    .lyrics-box { 
        background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 15px; 
        border-left: 5px solid #00f2ff; color: #eee; font-family: 'Courier New', monospace; 
        margin-top: 20px; border-right: 1px solid #333; line-height: 1.6;
    }
    /* Knappar */
    .stButton>button {
        background: rgba(0, 242, 255, 0.05); color: #00f2ff; 
        border: 2px solid #00f2ff; width: 100%; font-weight: bold; 
        border-radius: 12px; height: 3.8em; text-transform: uppercase; letter-spacing: 3px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background: #00f2ff; color: #000; box-shadow: 0px 0px 40px #00f2ff;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: #000 !important; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing: 10px; font-weight:bold;">MEGA AI ENGINE // FULL EDITION</p></div>', unsafe_allow_html=True)

# HJÄLPFUNKTION
def get_url(output):
    if isinstance(output, list): return str(output[0])
    if hasattr(output, 'url'): return str(output.url)
    return str(output)

# --- 2. SIDOMENY ---
with st.sidebar:
    st.header("⚡ KONTROLLPANEL")
    in_lang = st.selectbox("Ditt språk:", ["Svenska", "English", "Español", "日本語"])
    out_lang = st.selectbox("AI-språk:", ["Svenska", "English", "Español", "Français", "日本語"])
    st.divider()
    m_voice = st.radio("Röstkaraktär:", ["Kvinna", "Man"])
    st.info("Systemet pausar automatiskt mellan AI-steg för att skydda ditt konto.")

# API-NYCKEL
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_ok = True
else:
    st.error("⚠️ Saknar API-nyckel i Secrets!")
    api_ok = False

# --- 3. FUNKTIONER ---
if api_ok:
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK"])

    with tab1:
        c1, c2 = st.columns([1, 1.2])
        with c1:
            m_ide = st.text_area(f"Vad ska vi skapa? ({in_lang}):", "En futuristisk cyberpunk-stad i regnet", key="t_ide")
            m_stil = st.selectbox("Stil:", ["Cyberpunk", "Cinematic", "Anime", "Vintage 8mm"], key="t_stil")
            if st.button("🚀 STARTA PRODUKTION", key="t_btn"):
                with st.status("🏗️ Bygger mästerverk...", expanded=True) as status:
                    try:
                        # STEG 1: BILD
                        status.write("🎨 Skapar bild...")
                        img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                        img_url = get_url(img_raw)
                        
                        time.sleep(10) # Rate-limit skydd
                        
                        # STEG 2: TEXT
                        status.write("✍️ Skriver text...")
                        lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 short rhyming lines in {out_lang} about: {m_ide}. ONLY lyrics.", "max_new_tokens": 80})
                        lyrics = "".join(lyrics_res).replace('"', '').strip()
                        
                        time.sleep(10)

                        # STEG 3: VIDEO
                        status.write("📽️ Animerar...")
                        v_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic slow zoom", "first_frame_image": img_url}))
                        
                        time.sleep(10)

                        # STEG 4: MUSIK
                        status.write("🎵 Komponerar musik...")
                        m_url = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": f"{m_stil} style, melodic", "duration": 8}))

                        # STEG 5: MIXNING
                        status.write("🧪 Slutför mixning...")
                        with open("temp_v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("temp_a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("temp_v.mp4")
                        audio = AudioFileClip("temp_a.mp3")
                        if audio.duration > clip.duration: clip = clip.fx(vfx.loop, duration=audio.duration)
                        else: audio = audio.set_duration(clip.duration)
                        
                        clip.set_audio(audio).write_videofile("final_tomingai.mp4", codec="libx264", audio_codec="aac", logger=None)
                        status.update(label="✅ KLART!", state="complete")
                        
                        with c2:
                            st.video("final_tomingai.mp4")
                            st.markdown(f'<div class="lyrics-box"><b>🎵 LYRICS:</b><br>{lyrics}</div>', unsafe_allow_html=True)
                            with open("final_tomingai.mp4", "rb") as f:
                                st.download_button("💾 LADDA NER", f, "tomingai.mp4")
                    except Exception as e: st.error(f"Fel: {e}")

    # --- ENKLARE FLIKAR ---
    with tab2:
        up_img = st.file_uploader("Ladda upp bild", type=["jpg", "png"])
        if up_img and st.button("🎬 ANIMERA BILD"):
            with st.spinner("Jobbar..."):
                res_v = get_url(replicate.run("minimax/video-01", input={"first_frame_image": up_img}))
                st.video(res_v)

    with tab3:
        mu_in = st.text_input("Musik-prompt:")
        if st.button("🎧 SKAPA LJUD"):
            with st.spinner("Komponerar..."):
                res_m = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": mu_in, "duration": 10}))
                st.audio(res_m)

st.markdown("<br><center><small>TOMINGAI MEGA ENGINE v2.5 | 2024</small></center>", unsafe_allow_html=True)


















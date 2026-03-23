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
    .neon-title { font-family: 'Arial Black', sans-serif; font-size: 75px; font-weight: 900; color: #ffffff; text-transform: uppercase; letter-spacing: 10px; line-height: 1; margin: 0; text-shadow: 0 0 10px #fff, 0 0 40px #00f2ff, 0 0 80px #00f2ff; }
    .stTabs [data-baseweb="tab"] { height: auto; white-space: normal; padding: 10px 20px; background-color: #111; color: #eee; border-radius: 10px 10px 0 0; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; border-radius: 8px; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px; margin-top:20px;">GLOBAL AI ENGINE // MASTER STUDIO</p></div>', unsafe_allow_html=True)

def get_url(output):
    if isinstance(output, list): return str(output[0])
    if hasattr(output, 'url'): return str(output.url)
    return str(output)

with st.sidebar:
    st.header("🌍 Språk-Motor")
    in_lang = st.selectbox("Jag skriver på:", ["Svenska", "English", "Español"])
    out_lang = st.selectbox("AI:n sjunger på:", ["English", "Svenska", "Español"])
    st.divider()
    m_voice = st.radio("Välj röst:", ["Kvinna", "Man"])

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            m_ide = st.text_area(f"Idé på {in_lang}:", "En vacker natt i Tokyo", key="m_ide")
            m_stil = st.selectbox("Stil:", ["Cyberpunk", "Cinematic", "Anime"], key="m_stil")
        with col2:
            if st.button("🚀 SKAPA MAGI", key="m_btn"):
                with st.status("Producerar...") as status:
                    try:
                        img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                        img_url = get_url(img_raw)
                        st.image(img_url)
                        
                        lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 short rhyming lines in {out_lang} about '{m_ide}'. ONLY lyrics."})
                        lyrics = "".join(lyrics_res).replace('"', '')
                        
                        v_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url}))
                        
                        # Felsäkert musik-anrop
                        m_url = get_url(replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": f"{m_stil} style, {m_voice} vocals", "duration": 8}))
                        
                        with open("v1.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a1.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        clip = VideoFileClip("v1.mp4")
                        audio = AudioFileClip("a1.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out1.mp4", codec="libx264", audio_codec="aac")
                        st.video("out1.mp4")
                    except Exception as e:
                        st.error(f"Ett fel uppstod: {e}")

    with tab2:
        st.info("Regissören är redo.")
    with tab3:
        # BARA MUSIK - FELSÄKER VERSION
        if st.button("🎵 GENERERA LÅT", key="mus_btn"):
            with st.status("Komponerar..."):
                try:
                    mus_res = replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": "Swedish pop piano", "duration": 10})
                    st.audio(get_url(mus_res))
                except Exception as e:
                    st.error(f"Musik-fel: {e}")
else:
    st.error("⚠️ Kontrollera Secrets.")














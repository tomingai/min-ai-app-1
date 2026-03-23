import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & ULTRA-CLEAR NEON DESIGN ---
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
        font-family: 'Arial Black', sans-serif; font-size: 75px; font-weight: 900;
        color: #ffffff; text-transform: uppercase; letter-spacing: 10px;
        line-height: 1; margin: 0;
        text-shadow: 0 0 10px #fff, 0 0 40px #00f2ff, 0 0 80px #00f2ff;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        height: auto; white-space: normal; padding: 10px 20px;
        min-width: 150px; background-color: #111; color: #eee; border-radius: 10px 10px 0 0;
    }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button {
        background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff;
        width: 100%; font-weight: bold; border-radius: 8px;
    }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px; margin-top:20px;">GLOBAL AI ENGINE // TRIPLE MODE</p></div>', unsafe_allow_html=True)

# --- SIDOMENY ---
with st.sidebar:
    st.header("🌍 Språk-Motor")
    in_lang = st.selectbox("Jag skriver på:", ["Svenska", "English", "Español", "Français", "日本語", "Deutsch"])
    out_lang = st.selectbox("AI:n ska sjunga på:", ["English", "Svenska", "Español", "Français", "日本語", "Italiano"])
    st.divider()
    st.header("🎤 Röstprofil")
    m_voice = st.radio("Välj röst:", ["Kvinna", "Man"])

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK"])

    # --- FLIK 1: TOTAL MAGI ---
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            m_ide = st.text_area(f"Beskriv din idé på {in_lang}:", f"En vacker natt i Tokyo", key="m_ide")
            m_stil = st.selectbox("Välj stil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Anime"], key="m_stil")
        with col2:
            if st.button("🚀 SKAPA MAGI", key="m_btn"):
                with st.status(f"Producerar på {out_lang}...") as status:
                    # FIX: Hantera FLUX bild-output korrekt
                    img_output = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                    img_url = img_output[0] if isinstance(img_output, list) else img_output
                    st.image(img_url)
                    
                    lyrics = "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Based on '{m_ide}', write 4 short rhyming lines in {out_lang}. ONLY lyrics."})).replace('"', '')
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url}))
                    m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{m_stil} style, {m_voice} vocals", "lyrics": lyrics}))
                    
                    with open("v1.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a1.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v1.mp4")
                    audio = AudioFileClip("a1.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out1.mp4", codec="libx264", audio_codec="aac")
                    
                    st.video("out1.mp4")
                    with open("out1.mp4", "rb") as f:
                        st.download_button("💾 LADDA NER VIDEO", f, "tomingai_magic.mp4")

    # --- FLIK 2: REGISSÖREN ---
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            bild = st.file_uploader("Ladda upp egen bild", type=["jpg", "png", "jpeg"], key="r_img")
            if bild: st.image(bild, use_container_width=True)
        with col2:
            r_ide = st.text_input(f"Låtens handling ({in_lang}):", "En sång om mig själv", key="r_ide")
            if st.button("⚡ PRODUCERA", key="r_btn"):
                if bild:
                    with st.status(f"Jobbar på {out_lang}..."):
                        lyrics = "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Write 4 rhyming lines in {out_lang} about '{r_ide}'."})).replace('"', '')
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": bild}))
                        m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"Cinematic style, {m_voice} vocals", "lyrics": lyrics}))
                        with open("v2.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a2.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        clip = VideoFileClip("v2.mp4")
                        audio = AudioFileClip("a2.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out2.mp4", codec="libx264", audio_codec="aac")
                        st.video("out2.mp4")
                        with open("out2.mp4", "rb") as f:
                            st.download_button("💾 LADDA NER VIDEO", f, "tomingai_director.mp4")
                else: st.error("Ladda upp en bild!")

    # --- FLIK 3: BARA MUSIK ---
    with tab3:
        mus_col1, mus_col2 = st.columns(2)
        with mus_col1:
            mus_ide = st.text_area(f"Låtens handling ({in_lang}):", "En dröm om framtiden", key="mus_ide")
        with mus_col2:
            if st.button("🎵 GENERERA LÅT", key="mus_btn"):
                with st.status(f"Sjunger på {out_lang}..."):
                    mus_lyrics = "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Write 6 rhyming lines in {out_lang} about '{mus_ide}'."})).replace('"', '')
                    mus_res = replicate.run("minimax/music-1.5", input={"prompt": f"Studio quality, {m_voice} vocals", "lyrics": mus_lyrics})
                    st.audio(mus_res.url)
                    st.download_button("💾 LADDA NER MP3", requests.get(mus_res.url).content, "tomingai_song.mp3")

else:
    st.error("⚠️ Kontrollera REPLICATE_API_TOKEN i Secrets.")









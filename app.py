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
        text-align: center; margin-bottom: 30px;
    }
    .neon-title { font-family: 'Arial Black', sans-serif; font-size: 60px; font-weight: 900; color: #fff; text-shadow: 0 0 20px #00f2ff; margin: 0; }
    
    /* Textspalt-styling */
    .lyrics-box {
        background-color: #111;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00f2ff;
        color: #eee;
        font-family: 'Courier New', Courier, monospace;
        margin-top: 20px;
    }
    
    /* Flik-fix */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff;">MEGA AI ENGINE // TRIPLE MODE & LYRICS</p></div>', unsafe_allow_html=True)

# Sidomeny
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

    # --- FLIK 1: MAGI ---
    with tab1:
        col_in, col_out = st.columns(2)
        with col_in:
            m_ide = st.text_area(f"Din idé på {in_lang}:", "En vacker natt i Tokyo", key="m_ide")
            m_stil = st.selectbox("Musikstil:", ["Cyberpunk", "Cinematic", "Anime"], key="m_stil")
            if st.button("🚀 SKAPA MAGI", key="m_btn"):
                with st.status("Producerar...") as status:
                    # 1. Bild
                    img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                    img_url = img_raw[0] if isinstance(img_raw, list) else str(img_raw)
                    # 2. Text
                    lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 lines in {out_lang} about '{m_ide}'. ONLY lyrics."})
                    lyrics = "".join(lyrics_res).replace('"', '').strip()
                    # 3. Video & Musik
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url}))
                    m_url = str(replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": f"{m_stil} style, {m_voice} vocals", "duration": 8}))
                    # 4. Mix
                    with open("v1.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a1.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v1.mp4")
                    audio = AudioFileClip("a1.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out1.mp4", codec="libx264", audio_codec="aac")
                    with col_out:
                        st.video("out1.mp4")
                        st.markdown(f'<div class="lyrics-box"><b>🎵 Sångtext ({out_lang}):</b><br><br>{lyrics.replace("\n", "<br>")}</div>', unsafe_allow_html=True)

    # --- FLIK 2: REGISSÖREN ---
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            bild = st.file_uploader("Ladda upp egen bild", type=["jpg", "png", "jpeg"], key="r_img")
            if bild: st.image(bild, use_container_width=True)
        with col2:
            r_ide = st.text_input(f"Handling ({in_lang}):", "En sång om mig", key="r_ide")
            if st.button("⚡ PRODUCERA", key="r_btn"):
                if bild:
                    with st.status("Jobbar..."):
                        lyrics_r = "".join(replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 lines in {out_lang} about '{r_ide}'."})).replace('"', '')
                        v_res = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": bild}))
                        m_res = str(replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": "Cinematic", "duration": 8}))
                        with open("v2.mp4", "wb") as f: f.write(requests.get(v_res).content)
                        with open("a2.mp3", "wb") as f: f.write(requests.get(m_res).content)
                        clip2 = VideoFileClip("v2.mp4")
                        audio2 = AudioFileClip("a2.mp3").set_duration(clip2.duration)
                        clip2.set_audio(audio2).write_videofile("out2.mp4", codec="libx264", audio_codec="aac")
                        st.video("out2.mp4")
                        st.markdown(f'<div class="lyrics-box"><b>🎵 Sångtext:</b><br>{lyrics_r}</div>', unsafe_allow_html=True)

    # --- FLIK 3: BARA MUSIK ---
    with tab3:
        if st.button("🎵 GENERERA LÅT", key="mus_btn"):
            with st.status("Komponerar..."):
                mus_res = replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": "Pop piano", "duration": 10})
                st.audio(str(mus_res))
else:
    st.error("⚠️ Kontrollera Secrets.")















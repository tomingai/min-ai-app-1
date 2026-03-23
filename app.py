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
        text-align: center; margin-bottom: 30px;
    }
    .neon-title { font-family: 'Arial Black', sans-serif; font-size: 60px; font-weight: 900; color: #fff; text-shadow: 0 0 20px #00f2ff; margin: 0; }
    .lyrics-box { background-color: #111; padding: 20px; border-radius: 15px; border-left: 5px solid #00f2ff; color: #eee; font-family: 'Courier New', monospace; margin-top: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; border-radius: 8px; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff;">MEGA AI ENGINE // ALL MODES ACTIVE</p></div>', unsafe_allow_html=True)

# Sidomeny
with st.sidebar:
    st.header("🌍 Språk-Motor")
    in_lang = st.selectbox("Jag skriver på:", ["Svenska", "English", "Español"])
    out_lang = st.selectbox("AI:n ska sjunga på:", ["English", "Svenska", "Español"])
    st.divider()
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
        col_in, col_out = st.columns(2)
        with col_in:
            st.subheader("1. Beskriv din vision")
            m_ide = st.text_area(f"Vad ska filmen handla om? ({in_lang}):", "En futuristisk stad i regn", key="m_ide")
            m_stil = st.selectbox("Filmstil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Anime"], key="m_stil")
            if st.button("🚀 SKAPA MAGI", key="m_btn"):
                with st.status("AI-hjärnan skapar allt...") as status:
                    img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                    img_url = img_raw if isinstance(img_raw, list) else str(img_raw)
                    lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 rhyming lines in {out_lang} about '{m_ide}'. ONLY lyrics."})
                    lyrics = "".join(lyrics_res).replace('"', '').strip()
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url}))
                    m_url = str(replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": f"{m_stil} style, {m_voice} vocals", "duration": 8}))
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
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.subheader("1. Ladda upp din bild")
            bild = st.file_uploader("Välj en bild att animera", type=["jpg", "png", "jpeg"], key="r_img")
            if bild: st.image(bild, use_container_width=True)
        with col_r2:
            st.subheader("2. Regissörens instruktioner")
            r_handling = st.text_input(f"Vad ska låten handla om? ({in_lang})", "En sång om livet", key="r_ide")
            r_stil = st.selectbox("Välj musikstil:", ["Pop", "Cyberpunk", "Jazz", "Epic"], key="r_stil_regi")
            if st.button("⚡ PRODUCERA FILM", key="r_btn"):
                if bild:
                    with st.status("Producerar din film..."):
                        lyrics_r = "".join(replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 rhyming lines in {out_lang} about '{r_handling}'."})).replace('"', '')
                        v_r_url = str(replicate.run("minimax/video-01", input={"prompt": "Slow cinematic movement", "first_frame_image": bild}))
                        m_r_url = str(replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": f"{r_stil} style", "duration": 8}))
                        with open("v2.mp4", "wb") as f: f.write(requests.get(v_r_url).content)
                        with open("a2.mp3", "wb") as f: f.write(requests.get(m_r_url).content)
                        clip2 = VideoFileClip("v2.mp4")
                        audio2 = AudioFileClip("a2.mp3").set_duration(clip2.duration)
                        clip2.set_audio(audio2).write_videofile("out2.mp4", codec="libx264", audio_codec="aac")
                        st.video("out2.mp4")
                        st.markdown(f'<div class="lyrics-box"><b>🎵 Sångtext:</b><br>{lyrics_r}</div>', unsafe_allow_html=True)
                else: st.error("Du måste ladda upp en bild först!")

    # --- FLIK 3: BARA MUSIK ---
    with tab3:
        st.subheader("🎸 Skapa en unik låt")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            mus_ide = st.text_area(f"Beskriv låtens handling ({in_lang}):", "En dröm om framtiden", key="mus_ide")
            mus_stil = st.text_input("Musikstil & Instrument:", "Swedish Pop, Piano, Melodic", key="mus_stil")
        with m_col2:
            if st.button("🎵 GENERERA LÅT", key="mus_btn"):
                with st.status("AI:n komponerar..."):
                    mus_lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 6 rhyming lines in {out_lang} about '{mus_ide}'. ONLY lyrics."})
                    mus_lyrics = "".join(mus_lyrics_res).replace('"', '')
                    mus_res = str(replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": mus_stil, "duration": 15}))
                    st.audio(mus_res)
                    st.success(f"Sångtext ({out_lang}): {mus_lyrics}")
else:
    st.error("⚠️ Kontrollera REPLICATE_API_TOKEN i Secrets.")
















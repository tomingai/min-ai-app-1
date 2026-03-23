import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & ULTRA-CLEAR NEON DESIGN ---
st.set_page_config(page_title="TOMINGAI NEON STUDIO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    
    /* HD NEON LOGO */
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
    
    /* FIX FÖR ATT TEXTEN SKA SYNAS I FLIKARNA */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 10px; 
        justify-content: center; 
    }
    .stTabs [data-baseweb="tab"] {
        height: auto; 
        white-space: normal; /* Tillåter radbrytning */
        padding: 10px 20px;
        min-width: 150px;
        background-color: #111;
        color: #888;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #00f2ff !important; 
        color: black !important; 
        font-weight: bold; 
    }

    /* KNAPPAR */
    .stButton>button {
        background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff;
        width: 100%; font-weight: bold; border-radius: 8px;
    }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px; margin-top:20px;">MEGA AI ENGINE // TRIPLE MODE</p></div>', unsafe_allow_html=True)

# Hämta API-nyckel från Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    # KORTARE NAMN PÅ FLIKARNA SÅ DE FÅR PLATS BÄTTRE
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK"])

    # --- FLIK 1: TOTAL MAGI ---
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            m_ide = st.text_area(f"Beskriv din idé:", f"En vacker natt i Tokyo", key="m_ide")
            m_stil = st.selectbox("Välj stil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Anime"], key="m_stil")
        with col2:
            st.write("AI:n ritar, skriver och filmar allt åt dig.")
            if st.button("🚀 SKAPA MAGI", key="m_btn"):
                with st.status("Producerar...") as status:
                    img = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                    st.image(img)
                    lyrics = "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Write 4 short rhyming lines about '{m_ide}'. ONLY lyrics."})).replace('"', '')
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img}))
                    m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{m_stil} style", "lyrics": lyrics}))
                    with open("v1.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a1.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v1.mp4")
                    audio = AudioFileClip("a1.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out1.mp4", codec="libx264", audio_codec="aac")
                    st.video("out1.mp4")

    # --- FLIK 2: REGISSÖREN ---
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            bild = st.file_uploader("Ladda upp egen bild", type=["jpg", "png", "jpeg"], key="r_img")
            if bild: st.image(bild, use_container_width=True)
        with col2:
            r_ide = st.text_input(f"Vad ska låten handla om?", "En sång om mig själv", key="r_ide")
            r_stil = st.selectbox("Filmstil:", ["Cyberpunk", "Cinematic", "Anime"], key="r_stil")
            if st.button("⚡ PRODUCERA", key="r_btn"):
                if bild:
                    with st.status("Jobbar..."):
                        lyrics = "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Write 4 lines about '{r_ide}'."})).replace('"', '')
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": bild}))
                        m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{r_stil} style", "lyrics": lyrics}))
                        with open("v2.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a2.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        clip = VideoFileClip("v2.mp4")
                        audio = AudioFileClip("a2.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out2.mp4", codec="libx264", audio_codec="aac")
                        st.video("out2.mp4")
                else: st.error("Ladda upp en bild!")

    # --- FLIK 3: BARA MUSIK ---
    with tab3:
        st.subheader("🎸 Skapa enbart musik")
        mus_col1, mus_col2 = st.columns(2)
        with mus_col1:
            mus_ide = st.text_area(f"Låtens handling:", "En dröm om framtiden", key="mus_ide")
            mus_stil = st.text_input("Musikstil:", "Synthwave, 80s drums", key="mus_stil")
        with mus_col2:
            if st.button("🎵 GENERERA LÅT", key="mus_btn"):
                with st.status("Komponerar...") as status:
                    mus_lyrics = "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Write 6 lines about '{mus_ide}'."})).replace('"', '')
                    mus_res = replicate.run("minimax/music-1.5", input={"prompt": mus_stil, "lyrics": mus_lyrics})
                    st.audio(mus_res.url)
                    st.success(f"Sångtext: {mus_lyrics}")

else:
    st.error("⚠️ Kontrollera REPLICATE_API_TOKEN i Secrets.")









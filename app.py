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
    
    /* HD NEON LOGO - EXTRA TYDLIG */
    .neon-container {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #00f2ff;
        box-shadow: 0px 0px 40px rgba(0, 242, 255, 0.4);
        text-align: center;
        margin-bottom: 50px;
    }
    .neon-title {
        font-family: 'Arial Black', Gadget, sans-serif;
        font-size: 75px;
        font-weight: 900;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 10px;
        line-height: 1;
        margin: 0;
        text-shadow: 
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #00f2ff,
            0 0 82px #00f2ff;
    }
    .neon-subtitle {
        color: #00f2ff;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 12px;
        text-transform: uppercase;
        margin-top: 25px;
        opacity: 0.9;
        text-shadow: 0 0 5px #00f2ff;
    }
    
    /* FLIKAR & KNAPPAR */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; justify-content: center; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button {
        background-color: transparent;
        color: #00f2ff;
        border: 2px solid #00f2ff;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00f2ff;
        color: black;
        box-shadow: 0px 0px 20px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# Visa den suveräna logotypen
st.markdown("""
    <div class="neon-container">
        <p class="neon-title">TOMINGAI</p>
        <p class="neon-subtitle">A.I. NEON ENGINE // MASTER STUDIO</p>
    </div>
    """, unsafe_allow_html=True)

# Hämta API-nyckel automatiskt från Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    # SKAPA FLIKAR FÖR OLIKA LÄGEN
    tab1, tab2 = st.tabs(["🎬 MUSIKVIDEO (BILD + LJUD)", "🎧 BARA MUSIK (SINGEL)"])

    # --- FLIK 1: MUSIKVIDEO ---
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📡 DATAKÄLLA: BILD")
            bild = st.file_uploader("Ladda upp din startbild", type=["jpg", "png", "jpeg"], key="video_img")
            if bild: st.image(bild, use_container_width=True)
            
        with col2:
            st.subheader("🧠 PROCESSOR: MOVIE-MODE")
            v_stil = st.selectbox("Filmstil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Anime"], key="v_stil")
            v_lyr = st.text_area("Låttext (Lyrics):", "[Instrumental]", key="v_lyr", help="Skriv text för sång eller behåll [Instrumental]")
            v_rost = st.radio("Sångröst:", ["Kvinna (Female)", "Man (Male)"], key="v_rost", horizontal=True)
            
            if st.button("⚡ PRODUCERA MÄSTERVERK", key="v_btn"):
                if bild:
                    with st.status("INITIALISERAR FULL PRODUKTION...", expanded=True):
                        try:
                            # 1. Video (MiniMax)
                            v_url = str(replicate.run("minimax/video-01", input={"prompt": f"Cinematic movement, {v_stil} style, 4k", "first_frame_image": bild}))
                            # 2. Musik & Sång (MiniMax)
                            m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{v_stil} style, {v_rost} vocals", "lyrics": v_lyr}))
                            
                            # 3. Montering
                            with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                            with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                            clip = VideoFileClip("v.mp4")
                            audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                            clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                            
                            st.video("out.mp4")
                            st.download_button("💾 EXPORTERA MP4", open("out.mp4", "rb"), "tomingai_video.mp4")
                        except Exception as e:
                            st.error(f"SYSTEMFEL: {e}")
                else: st.error("Ladda upp en bild först!")

    # --- FLIK 2: BARA MUSIK ---
    with tab2:
        st.subheader("🎸 SKAPA EN UNIK LÅT (UTAN BILD)")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            m_genre = st.text_input("Genre & Instrument:", "Swedish Pop, Acoustic Guitar, Piano")
            m_mood = st.select_slider("Stämning:", options=["Dramatiskt", "Lugnt", "Energiskt", "Party!"])
            m_rost_only = st.radio("Välj röst:", ["Kvinna", "Man"], key="m_rost_only", horizontal=True)
        with m_col2:
            m_lyr_only = st.text_area("Skriv din låttext (Fulla verser):", "Här i nattens ljus, bygger vi vårt hus. \nKodens starka röst, ger mitt hjärta tröst.", key="m_lyr_only")
        
        if st.button("🎵 GENERERA LJUDSPÅR", key="m_only_btn"):
            with st.status("AI:N KOMPONERAR MUSIK..."):
                try:
                    music_res = replicate.run(
                        "minimax/music-1.5",
                        input={
                            "prompt": f"{m_genre}, {m_mood} mood, {m_rost_only} vocals, studio quality",
                            "lyrics": m_lyr_only
                        }
                    )
                    st.audio(music_res.url)
                    st.success("Ljudspåret är färdigt!")
                    st.download_button("💾 LADDA NER MP3", requests.get(music_res.url).content, "tomingai_song.mp3")
                except Exception as e:
                    st.error(f"MUSIKFEL: {e}")

else:
    st.error("⚠️ ÅTKOMST NEKAD: Kontrollera REPLICATE_API_TOKEN i Secrets.")







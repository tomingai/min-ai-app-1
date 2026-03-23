import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="TOMINGAI STUDIO PRO", page_icon="🎵", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    .neon-title { color: #fff; text-shadow: 0 0 20px #00f2ff; font-size: 40px; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #111; border-radius: 5px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="neon-title">⚡ TOMINGAI MULTI-STUDIO</p>', unsafe_allow_html=True)

# Hämta API-nyckel
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    # SKAPA FLIKAR
    tab1, tab2 = st.tabs(["🎬 MUSIKVIDEO (BILD + LJUD)", "🎧 BARA MUSIK (LÅTSKRIVARE)"])

    # --- FLIK 1: MUSIKVIDEO ---
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            bild = st.file_uploader("Ladda upp bild", type=["jpg", "png", "jpeg"], key="v_img")
            if bild: st.image(bild, use_container_width=True)
        with col2:
            v_style = st.selectbox("Stil:", ["Cyberpunk", "Cinematic", "Anime", "Vintage"], key="v_style")
            v_lyrics = st.text_area("Låttext (Sång):", "[Instrumental]", key="v_lyr")
            if st.button("🚀 SKAPA MUSIKVIDEO", key="v_btn"):
                if bild:
                    with st.status("Producerar film..."):
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": f"Cinematic movement, {v_style} style", "first_frame_image": bild}))
                        m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{v_style} soundtrack", "lyrics": v_lyrics}))
                        # Montering
                        with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        clip = VideoFileClip("v.mp4")
                        audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                        st.video("out.mp4")
                        st.download_button("💾 LADDA NER VIDEO", open("out.mp4", "rb"), "video.mp4")
                else: st.error("Ladda upp en bild!")

    # --- FLIK 2: BARA MUSIK ---
    with tab2:
        st.subheader("🎸 Skapa en unik låt")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            genre = st.text_input("Genre & Instrument:", "Swedish Pop, Acoustic Guitar, Piano")
            mood = st.select_slider("Känsla:", options=["Sorgligt", "Lugnt", "Glatt", "Party!"])
        with m_col2:
            m_lyrics = st.text_area("Din låttext (Lyrics):", "Här i nattens tysta timma, ser jag stjärnorna få glimma.", key="m_lyr_only")
            m_rost = st.radio("Sångröst:", ["Kvinna", "Man"], horizontal=True)

        if st.button("🎵 GENERERA LÅT", key="m_only_btn"):
            with st.status("AI:n komponerar och sjunger..."):
                try:
                    # Vi ber om en längre låt här
                    music_res = replicate.run(
                        "minimax/music-1.5",
                        input={
                            "prompt": f"{genre}, {mood} mood, {m_rost} vocals, high quality studio recording",
                            "lyrics": m_lyrics
                        }
                    )
                    st.audio(music_res.url)
                    st.success("Låten är klar!")
                    st.markdown(f"[🔗 Direktlänk till ljudfilen]({music_res.url})")
                except Exception as e:
                    st.error(f"Fel: {e}")

else:
    st.error("Nyckel saknas i Secrets!")







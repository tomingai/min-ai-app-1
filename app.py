import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN (HD NEON) ---
st.set_page_config(page_title="TOMINGAI NEON STUDIO", page_icon="⚡", layout="wide")

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
        text-shadow: 0 0 10px #fff, 0 0 40px #00f2ff, 0 0 80px #00f2ff;
    }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px;">A.I. MASTER STUDIO</p></div>', unsafe_allow_html=True)

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    tab1, tab2 = st.tabs(["🎬 MUSIKVIDEO", "🎧 BARA MUSIK"])

    # --- FLIK 1: MUSIKVIDEO ---
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            bild = st.file_uploader("Ladda upp bild", type=["jpg", "png", "jpeg"], key="v_img")
            if bild: st.image(bild, use_container_width=True)
        with col2:
            v_stil = st.selectbox("Stil:", ["Cyberpunk", "Cinematic", "Anime", "Vintage"], key="v_stil")
            v_input = st.text_input("Kort rad eller ord för låten:", "Sommarregn", key="v_input")
            
            if st.button("⚡ PRODUCERA VIDEO & MUSIK", key="v_btn"):
                with st.status("AI:n bygger ditt mästerverk...") as status:
                    # Steg 1: Skriv texten (Llama)
                    st.write("📝 Skriver låttext...")
                    lyrics_res = replicate.run("meta/meta-llama-3-70b-instruct", 
                        input={"prompt": f"Skriv 4 korta rimmade rader på svenska baserat på orden: {v_input}. Svara BARA med texten."})
                    final_lyrics = "".join(lyrics_res).replace('"', '')

                    # Steg 2: Skapa Video & Musik (MiniMax)
                    st.write("🎥 Genererar video...")
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": f"Cinematic movement, {v_stil} style", "first_frame_image": bild}))
                    st.write("🎵 Genererar sång...")
                    m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{v_stil} style", "lyrics": final_lyrics}))
                    
                    # Steg 3: Montering
                    with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v.mp4")
                    audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                    
                    st.video("out.mp4")
                    st.success(f"Text som skapades: {final_lyrics}")

    # --- FLIK 2: BARA MUSIK ---
    with tab2:
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            m_input = st.text_input("Dina ord (t.ex. 'Blåa ögon' eller 'Snabb bil'):", "Vinterstjärna", key="m_input")
            m_genre = st.text_input("Genre:", "Pop", key="m_genre")
        with m_col2:
            m_rost = st.radio("Röst:", ["Kvinna", "Man"], horizontal=True)
            
        if st.button("🎵 GENERERA LÅT", key="m_only_btn"):
            with st.status("Komponerar låt..."):
                # Skriv texten först
                lyrics_res = replicate.run("meta/meta-llama-3-70b-instruct", 
                    input={"prompt": f"Skriv en kort svensk låttext (4 rader) om: {m_input}. Svara BARA med texten."})
                final_m_lyrics = "".join(lyrics_res).replace('"', '')
                
                music_res = replicate.run("minimax/music-1.5", 
                    input={"prompt": f"{m_genre}, {m_rost} vocals", "lyrics": final_m_lyrics})
                
                st.audio(music_res.url)
                st.success(f"AI:n sjöng: {final_m_lyrics}")

else:
    st.error("Nyckel saknas i Secrets!")








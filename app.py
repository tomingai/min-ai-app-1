import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="TOMINGAI HYBRID STUDIO", page_icon="⚡", layout="wide")

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

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px;">A.I. HYBRID ENGINE</p></div>', unsafe_allow_html=True)

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI (TEXT ➔ ALLT)", "🎬 REGISSÖREN (BILD ➔ VIDEO)", "🎧 MUSIKSTUDION"])

    # --- FLIK 1: TOTAL MAGI ---
    with tab1:
        st.subheader("Skapa en hel film från en enda rad")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            magic_input = st.text_input("Vad ska filmen handla om?", "En rymdstation i neonljus", key="m_in")
            magic_stil = st.selectbox("Välj stil:", ["Cyberpunk", "Cinematic", "Anime", "Vintage"], key="m_stil")
        with m_col2:
            magic_rost = st.radio("Röst:", ["Kvinna", "Man"], horizontal=True, key="m_voice")
        
        if st.button("🚀 SKAPA MAGI", key="m_btn"):
            with st.status("AI-hjärnan skapar allt från grunden...") as status:
                try:
                    # 1. Bild (FLUX)
                    st.write("🎨 Ritar bilden...")
                    img_res = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{magic_input}, {magic_stil} style", "aspect_ratio": "16:9"})
                    st.image(img_res, caption="AI-genererad scen")
                    
                    # 2. Text (Llama)
                    st.write("📝 Skriver låttext...")
                    lyrics_res = replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Skriv 4 rimmade rader på svenska om: {magic_input}."})
                    final_lyr = "".join(lyrics_res).replace('"', '')

                    # 3. Video & Musik (MiniMax)
                    st.write("🎥 Animerar & Komponerar...")
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic motion", "first_frame_image": img_res}))
                    m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{magic_stil} style, {magic_rost} vocals", "lyrics": final_lyr}))

                    # 4. Mix
                    with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v.mp4")
                    audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                    st.video("out.mp4")
                    st.download_button("💾 LADDA NER", open("out.mp4", "rb"), "magic_film.mp4")
                except Exception as e: st.error(f"Fel: {e}")

    # --- FLIK 2: REGISSÖREN ---
    with tab2:
        st.subheader("Animera din egen bild")
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            bild = st.file_uploader("Ladda upp bild", type=["jpg", "png", "jpeg"], key="r_img")
            if bild: st.image(bild, use_container_width=True)
        with r_col2:
            r_prompt = st.text_input("Beskriv rörelsen:", "Slow cinematic zoom", key="r_prompt")
            r_lyr = st.text_area("Låttext:", "[Instrumental]", key="r_lyr")
            if st.button("⚡ PRODUCERA", key="r_btn"):
                if bild:
                    with st.status("Producerar..."):
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": r_prompt, "first_frame_image": bild}))
                        m_url = str(replicate.run("minimax/music-1.5", input={"prompt": "Cinematic", "lyrics": r_lyr}))
                        # (Samma mixning som ovan...)
                        with open("v2.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a2.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        clip = VideoFileClip("v2.mp4")
                        audio = AudioFileClip("a2.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out2.mp4", codec="libx264", audio_codec="aac")
                        st.video("out2.mp4")
                else: st.error("Ladda upp en bild!")

    # --- FLIK 3: MUSIKSTUDION ---
    with tab3:
        st.subheader("Skapa enbart musik")
        m_input = st.text_input("Vad ska låten handla om?", "En dröm om sommaren", key="m_only_in")
        m_style = st.text_input("Genre:", "Swedish Pop", key="m_only_style")
        if st.button("🎵 GENERERA LÅT", key="m_only_btn"):
            with st.status("Komponerar..."):
                lyrics_res = replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": f"Skriv en kort svensk låttext om: {m_input}."})
                final_m_lyr = "".join(lyrics_res).replace('"', '')
                music_res = replicate.run("minimax/music-1.5", input={"prompt": m_style, "lyrics": final_m_lyr})
                st.audio(music_res.url)
                st.success(f"Sångtext: {final_m_lyr}")

else:
    st.error("Nyckel saknas i Secrets!")








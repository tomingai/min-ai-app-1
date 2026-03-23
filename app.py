import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="TOMINGAI NEON STUDIO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    .neon-wrapper {
        background-color: #0a0a0a; padding: 30px; border-radius: 15px;
        border: 1px solid #00f2ff; box-shadow: 0px 0px 20px #00f2ff;
        text-align: center; margin-bottom: 40px;
    }
    .neon-text {
        font-family: 'Courier New', Courier, monospace; font-size: 50px;
        font-weight: 900; color: #fff; text-shadow: 0 0 20px #00f2ff; margin: 0;
    }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 15px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-wrapper"><p class="neon-text">TOMINGAI</p><p style="color:#00f2ff;">A.I. AUTO-DIRECTOR ENGINE</p></div>', unsafe_allow_html=True)

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📡 DATAKÄLLA: BILD")
        bild = st.file_uploader("Ladda upp bild", type=["jpg", "png", "jpeg"])
        if bild: 
            st.image(bild, use_container_width=True)
            if st.button("🪄 SKAPA MAGISKT MANUS & TEXT"):
                with st.spinner("AI:n analyserar bilden och skriver..."):
                    try:
                        # AI:n analyserar bilden (Llava)
                        analysis = replicate.run(
                            "yorickvp/llava-v1.6-vicuna-13b:0603dec596080305cb121a65853cd3578513d773528f9e0e6aa2f5d04ac838ad",
                            input={"image": bild, "prompt": "Describe a cinematic camera movement for this image. Keep it short and in English."}
                        )
                        st.session_state['ai_v_prompt'] = "".join(analysis)
                        
                        # AI:n skriver låttext (Llama 3)
                        lyrics_ai = replicate.run(
                            "meta/meta-llama-3-70b-instruct",
                            input={"prompt": f"Write 4 short rhyming lines in Swedish for a song about this scene: {st.session_state['ai_v_prompt']}. Poetic style.", "max_new_tokens": 100}
                        )
                        st.session_state['ai_lyrics'] = "".join(lyrics_ai)
                        st.rerun()
                    except Exception as e:
                        st.error(f"AI-fel: {e}")

    with col2:
        st.subheader("🧠 PROCESSOR: AUTOMANUS")
        stil = st.selectbox("Filmstil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Anime", "Pop Art"])
        
        # Dessa rutor fylls i automatiskt av den magiska staven
        v_prompt = st.text_input("Kamerarörelse (AI-genererad):", st.session_state.get('ai_v_prompt', "Slow cinematic zoom"))
        lyrics = st.text_area("Låttext (AI-genererad):", st.session_state.get('ai_lyrics', "[Instrumental]"))
        
        if st.button("⚡ PRODUCERA MÄSTERVERK"):
            if not bild:
                st.error("Ladda upp en bild först!")
            else:
                with st.status("PROSESSERAR NEON-DATA...", expanded=True):
                    try:
                        # 1. Video (MiniMax)
                        st.write("🎥 Genererar video...")
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": f"{v_prompt}, in {stil} style", "first_frame_image": bild}))

                        # 2. Musik (MiniMax)
                        st.write("🎵 Komponerar musik & sång...")
                        m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{stil} soundtrack", "lyrics": lyrics}))

                        # 3. Montering
                        st.write("✂️ Synkar ljud och bild...")
                        with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v.mp4")
                        audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                        
                        st.video("out.mp4")
                        with open("out.mp4", "rb") as f:
                            st.download_button("💾 EXPORTERA", f, "tomingai_master.mp4")
                    except Exception as e:
                        st.error(f"SYSTEMFEL: {e}")
else:
    st.error("⚠️ ÅTKOMST NEKAD: Lägg till REPLICATE_API_TOKEN i Streamlit Secrets.")







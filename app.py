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
    
    /* Textspalt-styling */
    .lyrics-box {
        background-color: #111;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #00f2ff;
        color: #eee;
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.6;
        min-height: 300px;
    }
    .lyrics-label { color: #00f2ff; font-weight: bold; text-transform: uppercase; font-size: 12px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff;">MEGA AI ENGINE // LYRICS EDITION</p></div>', unsafe_allow_html=True)

# Sidomeny för språk
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
    tab1, tab2 = st.tabs(["🪄 TOTAL MAGI", "🎧 BARA MUSIK"])

    with tab1:
        col_in, col_out = st.columns([1, 1]) # Skapar två stora spalter
        
        with col_in:
            st.subheader("📝 Din Idé")
            m_ide = st.text_area(f"Beskriv scenen på {in_lang}:", "En vacker natt i Tokyo", key="m_ide")
            m_stil = st.selectbox("Musikstil:", ["Cyberpunk", "Cinematic", "Anime"], key="m_stil")
            run_btn = st.button("🚀 SKAPA MÄSTERVERK", key="m_btn")

        with col_out:
            st.subheader("🎬 Resultat & Textspalt")
            output_placeholder = st.empty() # Här hamnar videon och texten sen
            
        if run_btn:
            with st.status("AI-studion jobbar...") as status:
                try:
                    # 1. Bild
                    img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                    img_url = img_raw[0] if isinstance(img_raw, list) else str(img_raw)
                    
                    # 2. Text (Llama)
                    lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 rhyming lines in {out_lang} about '{m_ide}'. ONLY lyrics."})
                    lyrics = "".join(lyrics_res).replace('"', '').strip()
                    
                    # 3. Video & Musik
                    v_url = str(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url}))
                    # MusicGen för stabilitet
                    m_url = str(replicate.run("facebookresearch/musicgen:7b3212fb7983471439735c0529d06634", input={"prompt": f"{m_stil} style, {m_voice} vocals", "duration": 8}))
                    
                    # 4. Mixning
                    with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v.mp4")
                    audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("final.mp4", codec="libx264", audio_codec="aac")
                    
                    # Visa i den högra spalten (col_out)
                    with col_out:
                        st.video("final.mp4")
                        st.markdown(f"""
                        <div class="lyrics-box">
                            <p class="lyrics-label">🎵 Sångtext ({out_lang})</p>
                            {lyrics.replace('\n', '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Ett fel uppstod: {e}")

    with tab2:
        st.info("Musikfliken är redo för nästa steg.")

else:
    st.error("⚠️ Kontrollera Secrets.")















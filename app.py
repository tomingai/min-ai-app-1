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
        text-align: center; margin-bottom: 50px;
    }
    .neon-title {
        font-family: 'Arial Black', sans-serif; font-size: 75px; font-weight: 900;
        color: #ffffff; text-transform: uppercase; letter-spacing: 10px;
        line-height: 1; margin: 0;
        text-shadow: 0 0 10px #fff, 0 0 40px #00f2ff, 0 0 80px #00f2ff;
    }
    .stTabs [data-baseweb="tab"] { height: auto; white-space: normal; padding: 10px 20px; background-color: #111; color: #eee; border-radius: 10px 10px 0 0; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; border-radius: 8px; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px; margin-top:20px;">GLOBAL AI ENGINE // TRIPLE MODE</p></div>', unsafe_allow_html=True)

# HJÄLPFUNKTION FÖR ATT HÄMTA REN URL
def get_url(output):
    if isinstance(output, list):
        return str(output[0])
    if hasattr(output, 'url'):
        return str(output.url)
    return str(output)

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

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            m_ide = st.text_area(f"Beskriv din idé på {in_lang}:", f"En vacker natt i Tokyo", key="m_ide")
            m_stil = st.selectbox("Välj stil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Anime"], key="m_stil")
        with col2:
            if st.button("🚀 SKAPA MAGI", key="m_btn"):
                with st.status(f"Producerar på {out_lang}...") as status:
                    # 1. RITA BILD (FLUX)
                    img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                    img_url = get_url(img_raw)
                    st.image(img_url, caption="AI-genererad scen")
                    
                    # 2. SKRIV TEXT (Bytt till Llama 3.1 för stabilitet)
                    lyrics_res = replicate.run(
                        "meta/meta-llama-3.1-405b-instruct", 
                        input={"prompt": f"Write 4 short rhyming lines in {out_lang} about '{m_ide}'. ONLY lyrics, no quotes."}
                    )
                    lyrics = "".join(lyrics_res).replace('"', '')
                    
                    # 3. GENERERA VIDEO & MUSIK
                    v_raw = replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url})
                    v_url = get_url(v_raw)
                    
                    m_raw = replicate.run("minimax/music-1.5", input={"prompt": f"{m_stil} style, {m_voice} vocals", "lyrics": lyrics})
                    m_url = get_url(m_raw)
                    
                    # 4. MONTERING
                    with open("v1.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a1.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    clip = VideoFileClip("v1.mp4")
                    audio = AudioFileClip("a1.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out1.mp4", codec="libx264", audio_codec="aac")
                    
                    st.video("out1.mp4")
                    st.download_button("💾 EXPORTERA", open("out1.mp4", "rb"), "tomingai_magic.mp4")

    # --- BEHÅLL FLIK 2 & 3 ---
    with tab2: st.info("Flik 2 är redo för dina egna bilder.")
    with tab3: st.info("Flik 3 är redo för din musik.")

else:
    st.error("⚠️ Kontrollera Secrets.")













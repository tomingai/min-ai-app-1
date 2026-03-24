import streamlit as st
import replicate
import os
import requests
import time
from moviepy.editor import VideoFileClip, AudioFileClip, vfx

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
    .lyrics-box { background-color: #111; padding: 20px; border-radius: 15px; border-left: 5px solid #00f2ff; color: #eee; font-family: 'Courier New', monospace; margin-top: 20px; border: 1px solid #333; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; border-radius: 8px; height: 3em; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing: 5px;">MEGA AI ENGINE // FULL EDITION</p></div>', unsafe_allow_html=True)

# HJÄLPFUNKTION FÖR ATT HÄMTA URL
def get_url(output):
    if isinstance(output, list): return str(output[0])
    if hasattr(output, 'url'): return str(output.url)
    return str(output)

# --- 2. SIDOMENY ---
with st.sidebar:
    st.header("🌍 Språk-Motor")
    in_lang = st.selectbox("Jag skriver på:", ["Svenska", "English", "Español", "日本語"])
    out_lang = st.selectbox("AI:n ska sjunga på:", ["Svenska", "English", "Español", "Français", "日本語"])
    st.divider()
    st.header("🎤 Röstprofil")
    m_voice = st.radio("Välj röstkaraktär:", ["Kvinna", "Man"])
    st.info("Obs: Pauser har lagts till för att hantera gratis-konton.")

# API-NYCKEL
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    st.error("⚠️ REPLICATE_API_TOKEN saknas i st.secrets!")
    api_key_found = False

if api_key_found:
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK"])

    # --- FLIK 1: TOTAL MAGI ---
    with tab1:
        col1, col2 = st.columns([1, 1.2])
        with col1:
            m_ide = st.text_area(f"Vad ska filmen handla om? ({in_lang}):", "En neonbelyst natt i Stockholm", key="m_ide")
            m_stil = st.selectbox("Visuell stil:", ["Cyberpunk", "Cinematic", "Anime", "Vintage 8mm"], key="m_stil")
            m_btn = st.button("🚀 SKAPA FULLSTÄNDIG PRODUKT", key="m_btn")

        if m_btn:
            with st.status("🛠️ Startar studion (väntetid inkluderad)...", expanded=True) as status:
                try:
                    # 1. Bild (Flux)
                    status.write("🎨 Steg 1: Skapar bild...")
                    img_raw = replicate.run("black-forest-labs/flux-schnell", 
                                          input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                    img_url = get_url(img_raw)
                    
                    status.write("⏳ Pausar för att inte överbelasta kontot...")
                    time.sleep(10) # Vänta på att rate limit återställs

                    # 2. Text (Llama)
                    status.write("✍️ Steg 2: Skriver sångtext...")
                    lyrics_res = replicate.run("meta/llama-2-70b-chat", 
                                             input={"prompt": f"Write 4 rhyming lines in {out_lang} about '{m_ide}'. ONLY lyrics."})
                    lyrics = "".join(lyrics_res).replace('"', '').strip()
                    
                    status.write("⏳ Pausar igen...")
                    time.sleep(10)

                    # 3. Video (Minimax)
                    status.write("📽️ Steg 3: Animerar video...")
                    v_url = get_url(replicate.run("minimax/video-01", 
                                               input={"prompt": "Cinematic camera movement", "first_frame_image": img_url}))
                    
                    status.write("⏳ En sista paus...")
                    time.sleep(10)

                    # 4. Musik (Musicgen)
                    status.write("🎵 Steg 4: Komponerar musik...")
                    m_url = get_url(replicate.run("facebookresearch/musicgen", 
                                               input={"prompt": f"{m_stil} style music, {m_voice} vocals", "duration": 8}))
                    
                    # 5. Mixning
                    status.write("🧪 Steg 5: Mixar slutprodukten...")
                    with open("v1.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a1.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    
                    clip = VideoFileClip("v1.mp4")
                    audio = AudioFileClip("a1.mp3").set_duration(clip.duration)
                    clip.set_audio(audio).write_videofile("out1.mp4", codec="libx264", audio_codec="aac", logger=None)
                    
                    status.update(label="✅ Allt klart!", state="complete")
                    
                    with col2:
                        st.video("out1.mp4")
                        st.markdown(f'<div class="lyrics-box"><b>🎵 LYRICS:</b><br>{lyrics}</div>', unsafe_allow_html=True)
                        with open("out1.mp4", "rb") as f:
                            st.download_button("💾 SPARA VIDEO", f, "tomingai.mp4")

                except Exception as e:
                    st.error(f"Fel: {e}. Pröva att vänta en minut och kör igen.")

    # --- FLIK 2: REGISSÖREN ---
    with tab2:
        st.write("Ladda upp en bild för att göra den till video.")
        bild_fil = st.file_uploader("Välj bild", type=["jpg", "png"])
        if bild_fil and st.button("⚡ GENERERA VIDEO"):
            with st.status("🎬 Behandlar..."):
                # Här kan du implementera liknande time.sleep om du kör flera steg
                v_r_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Slow motion", "first_frame_image": bild_fil}))
                st.video(v_r_url)

    # --- FLIK 3: BARA MUSIK ---
    with tab3:
        m_prompt = st.text_input("Vad för musik?")
        if st.button("🎵 SKAPA MUSIK"):
            with st.spinner("🎸 Komponerar..."):
                m_res = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": m_prompt, "duration": 10}))
                st.audio(m_res)
else:
    st.info("Lägg till din API-nyckel i .streamlit/secrets.toml för att börja.")

















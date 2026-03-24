import streamlit as st
import replicate
import os
import requests
import time
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
import datetime

# --- 1. SETUP & SESSION STATE (APPENS MINNE) ---
st.set_page_config(page_title="TOMINGAI MEGA STUDIO", page_icon="⚡", layout="wide")

if "gallery" not in st.session_state:
    st.session_state.gallery = []

# --- 2. AVANCERAD DESIGN (ANIMERAD BAKGRUND & NEON) ---
st.markdown("""
    <style>
    /* Animerad mörk gradient-bakgrund */
    .stApp {
        background: linear-gradient(125deg, #050505, #0a0a0a, #00151a, #050505);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #fff;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glas-effekt behållare */
    .neon-container {
        background: rgba(10, 10, 10, 0.85);
        padding: 40px; border-radius: 30px; 
        border: 1px solid rgba(0, 242, 255, 0.4);
        box-shadow: 0px 0px 60px rgba(0, 242, 255, 0.2);
        text-align: center; margin-bottom: 40px;
        backdrop-filter: blur(15px);
    }
    .neon-title { 
        font-family: 'Arial Black', sans-serif; font-size: 70px; font-weight: 900; 
        color: #fff; text-shadow: 0 0 10px #00f2ff, 0 0 30px #00f2ff; margin: 0; 
    }
    .lyrics-box { 
        background: rgba(20, 20, 20, 0.9); padding: 20px; border-radius: 12px; 
        border-left: 5px solid #00f2ff; color: #eee; font-family: 'Courier New', monospace; 
        margin-top: 15px; line-height: 1.5;
    }
    /* Knappar */
    .stButton>button {
        background: rgba(0, 242, 255, 0.05); color: #00f2ff; 
        border: 2px solid #00f2ff; width: 100%; font-weight: bold; 
        border-radius: 12px; height: 3.5em; text-transform: uppercase; letter-spacing: 2px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background: #00f2ff; color: #000; box-shadow: 0px 0px 40px #00f2ff;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: #000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing: 8px; font-weight:bold;">MEGA AI ENGINE // PROJECT EDITION</p></div>', unsafe_allow_html=True)

# HJÄLPFUNKTION FÖR URL:ER
def get_url(output):
    if isinstance(output, list): return str(output[0])
    if hasattr(output, 'url'): return str(output.url)
    return str(output)

# --- 3. SIDOMENY ---
with st.sidebar:
    st.header("⚡ STUDIO KONTROLL")
    in_lang = st.selectbox("Ditt språk:", ["Svenska", "English", "Español", "日本語"])
    out_lang = st.selectbox("AI-språk:", ["Svenska", "English", "Español", "Français", "日本語"])
    st.divider()
    m_voice = st.radio("Röstkaraktär:", ["Kvinna", "Man"])
    st.divider()
    if st.button("🗑️ RENSA BIBLIOTEK"):
        st.session_state.gallery = []
        st.rerun()

# API-NYCKEL KOLL
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_ready = True
else:
    st.error("Gå till Streamlit Secrets och lägg till REPLICATE_API_TOKEN!")
    api_ready = False

# --- 4. HUVUDAPPEN ---
if api_ready:
    tab1, tab2, tab3, tab4 = st.tabs(["🪄 SKAPA ALLT", "🎬 REGISSÖREN", "🎧 BARA MUSIK", "📚 BIBLIOTEK"])

    # --- FLIK 1: TOTAL MAGI ---
    with tab1:
        c1, c2 = st.columns([1, 1.2])
        with c1:
            proj_name = st.text_input("Namnge ditt projekt:", f"Mästerverk {len(st.session_state.gallery)+1}")
            m_ide = st.text_area(f"Beskriv din vision ({in_lang}):", "En neonstad i regnet")
            m_stil = st.selectbox("Stil:", ["Cyberpunk", "Cinematic", "Anime", "Vintage 8mm"])
            
            if st.button("🚀 STARTA FULL PRODUKTION"):
                with st.status("🏗️ Bygger projektet...", expanded=True) as status:
                    try:
                        # STEG 1: BILD
                        status.write("🎨 Genererar bild...")
                        img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"})
                        img_url = get_url(img_raw)
                        
                        time.sleep(10) # Rate limit skydd

                        # STEG 2: TEXT
                        status.write("✍️ Skriver text...")
                        lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 short rhyming lines in {out_lang} about: {m_ide}. ONLY lyrics.", "max_new_tokens": 100})
                        lyrics = "".join(lyrics_res).replace('"', '').strip()

                        time.sleep(10)

                        # STEG 3: VIDEO
                        status.write("📽️ Animerar...")
                        v_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url}))
                        
                        time.sleep(10)

                        # STEG 4: MUSIK
                        status.write("🎵 Komponerar musik...")
                        m_url = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": f"{m_stil} music, melodic", "duration": 8}))

                        # STEG 5: MIXNING & SPARA
                        status.write("🧪 Mixar slutprodukten...")
                        v_filename = f"proj_{int(time.time())}.mp4"
                        with open("v_tmp.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a_tmp.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v_tmp.mp4")
                        audio = AudioFileClip("a_tmp.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile(v_filename, codec="libx264", audio_codec="aac", logger=None)
                        
                        # Lägg till i biblioteket
                        st.session_state.gallery.append({
                            "name": proj_name,
                            "time": datetime.datetime.now().strftime("%H:%M"),
                            "prompt": m_ide,
                            "video": v_filename,
                            "lyrics": lyrics
                        })
                        
                        status.update(label="✅ PROJEKT KLART!", state="complete")
                        with c2:
                            st.video(v_filename)
                            st.markdown(f'<div class="lyrics-box"><b>{proj_name}</b><br>{lyrics}</div>', unsafe_allow_html=True)
                    except Exception as e: st.error(f"Fel: {e}")

    # --- FLIK 4: BIBLIOTEK ---
    with tab4:
        st.subheader("Ditt Projekt-Arkiv")
        if not st.session_state.gallery:
            st.info("Biblioteket är tomt.")
        else:
            for item in reversed(st.session_state.gallery):
                with st.expander(f"📁 {item['name']} ({item['time']})"):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.video(item['video'])
                    with col_b:
                        st.write(f"**Vision:** {item['prompt']}")
                        st.write(f"**Text:**\n{item['lyrics']}")
                        with open(item['video'], "rb") as f:
                            st.download_button(f"Ladda ner MP4", f, file_name=f"{item['name']}.mp4")

    # (Flik 2 & 3 implementeras på samma sätt med Replicate-anrop vid behov)
    with tab2: st.write("Här kan du ladda upp bilder och animera dem manuellt.")
    with tab3: st.write("Här genererar du bara ljudspår.")

st.markdown("<br><center><small>TOMINGAI MEGA ENGINE // 2024</small></center>", unsafe_allow_html=True)


















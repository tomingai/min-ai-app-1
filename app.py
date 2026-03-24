import streamlit as st
import replicate
import os
import requests
import time
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
import datetime

# --- 1. SETUP & SESSION STATE (APPENS MINNE) ---
st.set_page_config(page_title="MAXIMUSIKAI STUDIO", page_icon="🎵", layout="wide")

# Initiera minnen om de inte finns
if "gallery" not in st.session_state:
    st.session_state.gallery = []
if "community_feed" not in st.session_state:
    st.session_state.community_feed = []

# --- 2. DESIGN (MAXIMUSIKAI NEON THEME) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(125deg, #050505, #0a0a0a, #0b001a, #050505);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #fff;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .neon-container {
        background: rgba(10, 10, 10, 0.85);
        padding: 40px; border-radius: 30px; 
        border: 1px solid rgba(191, 0, 255, 0.4);
        box-shadow: 0px 0px 60px rgba(191, 0, 255, 0.2);
        text-align: center; margin-bottom: 40px;
        backdrop-filter: blur(15px);
    }
    .neon-title { 
        font-family: 'Arial Black', sans-serif; font-size: 70px; font-weight: 900; 
        color: #fff; text-shadow: 0 0 10px #bf00ff, 0 0 30px #bf00ff; margin: 0; 
    }
    .lyrics-box { 
        background: rgba(20, 20, 20, 0.9); padding: 20px; border-radius: 12px; 
        border-left: 5px solid #bf00ff; color: #eee; font-family: 'Courier New', monospace; 
        margin-top: 15px; line-height: 1.5;
    }
    .stButton>button {
        background: rgba(191, 0, 255, 0.05); color: #bf00ff; 
        border: 2px solid #bf00ff; width: 100%; font-weight: bold; 
        border-radius: 12px; height: 3.5em; text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover {
        background: #bf00ff; color: #000; box-shadow: 0px 0px 40px #bf00ff;
    }
    .stTabs [aria-selected="true"] { background-color: #bf00ff !important; color: #000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">MAXIMUSIKAI</p><p style="color:#bf00ff; letter-spacing: 8px; font-weight:bold;">ULTIMATE AI MUSIC & VIDEO STUDIO</p></div>', unsafe_allow_html=True)

# HJÄLPFUNKTION
def get_url(output):
    if isinstance(output, list): return str(output[0])
    if hasattr(output, 'url'): return str(output.url)
    return str(output)

# --- 3. SIDOMENY ---
with st.sidebar:
    st.header("⚡ MAXI CONTROL")
    in_lang = st.selectbox("Ditt språk:", ["Svenska", "English", "Español", "日本語"])
    out_lang = st.selectbox("AI-språk:", ["Svenska", "English", "Español", "Français", "日本語"])
    st.divider()
    m_voice = st.radio("Röstkaraktär:", ["Kvinna", "Man"])
    st.divider()
    if st.button("🗑️ NOLLSTÄLL ALLT"):
        st.session_state.gallery = []
        st.session_state.community_feed = []
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK", "📚 BIBLIOTEK", "🌐 COMMUNITY"])

    # --- FLIK 1: TOTAL MAGI ---
    with tab1:
        c1, c2 = st.columns([1, 1.2])
        with c1:
            proj_name = st.text_input("Projektets namn:", f"MAXI-PROJ {len(st.session_state.gallery)+1}")
            m_ide = st.text_area(f"Beskriv din vision ({in_lang}):", "En cyberpunk-stad i regnet")
            m_stil = st.selectbox("Stil:", ["Cyberpunk", "Cinematic", "Anime", "Vintage 8mm"])
            
            if st.button("🚀 STARTA FULL MAXI-PRODUKTION"):
                with st.status("🏗️ MAXIMUSIKAI bygger...", expanded=True) as status:
                    try:
                        # 1. BILD
                        status.write("🎨 Genererar bild...")
                        img_url = get_url(replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style", "aspect_ratio": "16:9"}))
                        time.sleep(10)

                        # 2. TEXT
                        status.write("✍️ Skriver text...")
                        lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 short rhyming lines in {out_lang} about: {m_ide}. ONLY lyrics.", "max_new_tokens": 100})
                        lyrics = "".join(lyrics_res).replace('"', '').strip()
                        time.sleep(10)

                        # 3. VIDEO
                        status.write("📽️ Animerar...")
                        v_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url}))
                        time.sleep(10)

                        # 4. MUSIK
                        status.write("🎵 Komponerar musik...")
                        m_url = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": f"{m_stil} style, melodic", "duration": 8}))

                        # 5. MIXNING
                        status.write("🧪 Mixar...")
                        v_filename = f"maxi_{int(time.time())}.mp4"
                        with open("v_tmp.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a_tmp.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v_tmp.mp4")
                        audio = AudioFileClip("a_tmp.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile(v_filename, codec="libx264", audio_codec="aac", logger=None)
                        
                        # Spara i Bibliotek
                        entry = {"name": proj_name, "time": datetime.datetime.now().strftime("%H:%M"), "prompt": m_ide, "video": v_filename, "lyrics": lyrics, "likes": 0}
                        st.session_state.gallery.append(entry)
                        
                        status.update(label="✅ KLART!", state="complete")
                        with c2:
                            st.video(v_filename)
                            st.markdown(f'<div class="lyrics-box"><b>{proj_name}</b><br>{lyrics}</div>', unsafe_allow_html=True)
                            if st.button("🌍 DELA TILL COMMUNITY"):
                                st.session_state.community_feed.append(entry)
                                st.success("Delad! Se fliken Community.")
                    except Exception as e: st.error(f"Fel: {e}")

    # --- FLIK 4: BIBLIOTEK ---
    with tab4:
        for item in reversed(st.session_state.gallery):
            with st.expander(f"📁 {item['name']} ({item['time']})"):
                st.video(item['video'])
                st.write(item['lyrics'])

    # --- FLIK 5: COMMUNITY ---
    with tab5:
        st.markdown("<h2 style='text-align:center; color:#bf00ff;'>🌐 COMMUNITY FEED</h2>", unsafe_allow_html=True)
        if not st.session_state.community_feed:
            st.info("Ingen har delat något än. Bli först!")
        else:
            for idx, post in enumerate(reversed(st.session_state.community_feed)):
                with st.container():
                    st.markdown(f"<div style='border:1px solid #bf00ff; padding:10px; border-radius:10px;'><h3>{post['name']}</h3>", unsafe_allow_html=True)
                    cv, ct = st.columns(2)
                    with cv: st.video(post['video'])
                    with ct: 
                        st.write(post['lyrics'])
                        if st.button(f"❤️ Gilla ({post['likes']})", key=f"like_{idx}"):
                            post['likes'] += 1
                            st.rerun()
                    st.markdown("</div><br>", unsafe_allow_html=True)

    # Flikar 2 & 3 (Förenklade)
    with tab2: st.info("Använd fliken TOTAL MAGI för full produktion.")
    with tab3: 
        if st.button("🎵 Generera snabb musik"):
            res = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": "Pop music", "duration": 5}))
            st.audio(res)

st.markdown("<br><center><small>MAXIMUSIKAI // 2024</small></center>", unsafe_allow_html=True)




















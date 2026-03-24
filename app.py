import streamlit as st
import replicate
import os
import requests
import time
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
import datetime

# Försök importera Supabase, men krascha inte om det saknas
try:
    from st_supabase_connection import SupabaseConnection
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# --- 1. SETUP ---
st.set_page_config(page_title="MAXIMUSIKAI STUDIO", page_icon="🎵", layout="wide")

# Koppla till Supabase om möjligt
db_ready = False
if SUPABASE_AVAILABLE:
    try:
        st_supabase = st.connection("supabase", type=SupabaseConnection)
        db_ready = True
    except:
        db_ready = False

# --- 2. DESIGN (LJUSA FLIKAR & NEON) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(125deg, #050505, #0a0a0a, #0b001a, #050505);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* FIX: EXTRA LJUS TEXT PÅ FLIKARNA */
    .stTabs [data-baseweb="tab"] {
        border-bottom: 2px solid transparent;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #FFFFFF !important; /* Kritvit */
        font-weight: 800 !important;
        font-size: 20px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #bf00ff !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #bf00ff !important; /* Neon vid val */
        text-shadow: 0 0 10px #bf00ff;
    }

    .neon-container {
        background: rgba(10, 10, 10, 0.85);
        padding: 35px; border-radius: 30px; 
        border: 2px solid rgba(191, 0, 255, 0.5);
        box-shadow: 0px 0px 50px rgba(191, 0, 255, 0.2);
        text-align: center; margin-bottom: 40px;
        backdrop-filter: blur(15px);
    }
    .neon-title { 
        font-family: 'Arial Black', sans-serif; font-size: 65px; font-weight: 900; 
        color: #fff; text-shadow: 0 0 15px #bf00ff; margin: 0; 
    }
    .stButton>button {
        background: rgba(191, 0, 255, 0.1); color: #bf00ff; 
        border: 2px solid #bf00ff; font-weight: bold; border-radius: 12px;
    }
    .stButton>button:hover {
        background: #bf00ff; color: #000; box-shadow: 0 0 30px #bf00ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">MAXIMUSIKAI</p></div>', unsafe_allow_html=True)

# HJÄLPFUNKTION
def get_url(output):
    if isinstance(output, list): return str(output[0])
    if hasattr(output, 'url'): return str(output.url)
    return str(output)

# --- 3. HUVUDAPPEN ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK", "📚 BIBLIOTEK", "🌐 COMMUNITY"])

with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        proj_name = st.text_input("Namnge projektet:", "MAXI PROJECT")
        m_ide = st.text_area("Beskrivning:", "En neonbelyst stad i framtiden")
        m_btn = st.button("🚀 STARTA")

    if m_btn:
        with st.status("🛠️ MAXIMUSIKAI arbetar...") as status:
            try:
                # API-anrop
                img_url = get_url(replicate.run("black-forest-labs/flux-schnell", input={"prompt": m_ide, "aspect_ratio": "16:9"}))
                time.sleep(10)
                
                v_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": img_url}))
                
                status.update(label="✅ PRODUKTION KLAR!", state="complete")
                with c2:
                    st.video(v_url)
                    if db_ready:
                        if st.button("🌍 PUBLICERA GLOBALT"):
                            st_supabase.table("posts").insert({"name": proj_name, "video_url": v_url, "likes": 0}).execute()
                            st.success("Delat till Community!")
            except Exception as e:
                st.error(f"Ett fel uppstod: {e}")

with tab5:
    st.markdown("<h2 style='text-align:center; color:#bf00ff;'>🌐 GLOBAL FEED</h2>", unsafe_allow_html=True)
    if db_ready:
        posts = st_supabase.table("posts").select("*").order("created_at", desc=True).execute().data
        for p in posts:
            with st.container():
                st.subheader(p['name'])
                st.video(p['video_url'])
                st.divider()
    else:
        st.info("Koppla Supabase i secrets för att se community-flödet.")

st.markdown("<br><center><small>MAXIMUSIKAI // 2024</small></center>", unsafe_allow_html=True)





















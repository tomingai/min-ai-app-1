import streamlit as st
import replicate
import os
import requests
import time
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
import datetime

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="MAXIMUSIKAI STUDIO", page_icon="🎵", layout="wide")

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
    
    /* EXTRA LJUSA OCH TYDLIGA FLIKAR */
    .stTabs [data-baseweb="tab"] p {
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        font-size: 24px !important; /* Större text */
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stTabs [aria-selected="true"] p {
        color: #bf00ff !important;
        text-shadow: 0 0 20px #bf00ff;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #bf00ff !important;
    }

    .neon-container {
        background: rgba(10, 10, 10, 0.85);
        padding: 40px; border-radius: 30px; 
        border: 2px solid rgba(191, 0, 255, 0.6);
        box-shadow: 0px 0px 60px rgba(191, 0, 255, 0.3);
        text-align: center; margin-bottom: 40px;
        backdrop-filter: blur(15px);
    }
    .neon-title { 
        font-family: 'Arial Black', sans-serif; font-size: 80px; font-weight: 900; 
        color: #fff; text-shadow: 0 0 15px #bf00ff, 0 0 40px #bf00ff; margin: 0; 
    }
    .stButton>button {
        background: rgba(191, 0, 255, 0.1); color: #bf00ff; 
        border: 2px solid #bf00ff; width: 100%; font-weight: bold; 
        border-radius: 12px; height: 3.5em; text-transform: uppercase;
    }
    .stButton>button:hover {
        background: #bf00ff; color: #000; box-shadow: 0px 0px 40px #bf00ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">MAXIMUSIKAI</p></div>', unsafe_allow_html=True)

# API KOLL
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_ready = True
else:
    st.error("Lägg till din Replicate-token i Secrets!")
    api_ready = False

# --- 2. HUVUDAPPEN ---
if api_ready:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK", "📚 BIBLIOTEK", "🌐 COMMUNITY"])

    with tab1:
        c1, c2 = st.columns([1, 1.2])
        with c1:
            m_ide = st.text_area("VAD SKALL VI SKAPA IDAG?", "En futuristisk stad i lila neon")
            if st.button("🚀 STARTA PRODUKTION"):
                with st.status("🏗️ MAXIMUSIKAI BYGGER...") as status:
                    # Logiken för generering här...
                    time.sleep(2)
                    status.update(label="✅ KLART!", state="complete")
                    st.success("DIN MUSIKVIDEO ÄR REDO!")

    with tab5:
        st.markdown("<h2 style='text-align:center; color:#bf00ff;'>🌐 COMMUNITY HUB</h2>", unsafe_allow_html=True)
        st.info("Här kommer vi dela allas musik när databasen är på plats!")

st.markdown("<br><center><small>MAXIMUSIKAI // 2024</small></center>", unsafe_allow_html=True)






















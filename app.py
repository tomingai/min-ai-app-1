import streamlit as st
import replicate
import os
import requests
import time
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
import datetime
from st_supabase_connection import SupabaseConnection

# --- 1. SETUP & DATABAS-ANSLUTNING ---
st.set_page_config(page_title="MAXIMUSIKAI STUDIO", page_icon="🎵", layout="wide")

# Koppla till Supabase (Riktig databas)
try:
    st_supabase = st.connection("supabase", type=SupabaseConnection)
    db_ready = True
except:
    db_ready = False

# --- 2. DESIGN (MED LJUSARE FLIK-TEXT) ---
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
    
    /* FIX: LJUSARE TEXT PÅ FLIKARNA */
    .stTabs [data-baseweb="tab"] p {
        color: #ffffff !important; /* Kritvit text */
        font-weight: 600 !important;
        font-size: 18px !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #bf00ff !important; /* Neon-lila när vald */
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
    .stButton>button {
        background: rgba(191, 0, 255, 0.05); color: #bf00ff; 
        border: 2px solid #bf00ff; width: 100%; border-radius: 12px; height: 3.5em;
    }
    .stButton>button:hover {
        background: #bf00ff; color: #000; box-shadow: 0px 0px 40px #bf00ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">MAXIMUSIKAI</p></div>', unsafe_allow_html=True)

# HJÄLPFUNKTION
def get_url(output):
    if isinstance(output, list): return str(output[0])
    return str(output)

# --- 3. HUVUDAPPEN ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK", "📚 MITT ARKIV", "🌐 COMMUNITY"])

with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        proj_name = st.text_input("Projektets namn:", "Mitt Mästerverk")
        m_ide = st.text_area("Beskriv din vision:", "En rymdresa genom nebulosor")
        if st.button("🚀 STARTA PRODUKTION"):
            with st.status("🏗️ MAXIMUSIKAI bygger...") as status:
                # 1. AI Logik (Samma som innan)
                img_url = get_url(replicate.run("black-forest-labs/flux-schnell", input={"prompt": m_ide, "aspect_ratio": "16:9"}))
                time.sleep(5)
                lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 lines about: {m_ide}. ONLY lyrics."})
                lyrics = "".join(lyrics_res).replace('"', '').strip()
                time.sleep(5)
                v_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic", "first_frame_image": img_url}))
                
                # Visa resultat
                status.update(label="✅ KLART!", state="complete")
                with c2:
                    st.video(v_url)
                    st.write(lyrics)
                    
                    # DELA TILL DATABAS
                    if db_ready:
                        if st.button("🌍 PUBLICERA GLOBALT"):
                            st_supabase.table("posts").insert({
                                "name": proj_name,
                                "video_url": v_url,
                                "lyrics": lyrics,
                                "likes": 0
                            }).execute()
                            st.success("Ditt verk ligger nu i Community-fliken för alla!")
                    else:
                        st.warning("Databasen är inte ansluten ännu.")

with tab5:
    st.markdown("<h2 style='text-align:center; color:#bf00ff;'>🌐 GLOBAL COMMUNITY FEED</h2>", unsafe_allow_html=True)
    if db_ready:
        # Hämta data från Supabase
        response = st_supabase.table("posts").select("*").order("created_at", desc=True).execute()
        posts = response.data
        
        for post in posts:
            with st.container():
                st.markdown(f"<div style='border:1px solid #bf00ff; padding:15px; border-radius:15px; margin-bottom:20px;'>", unsafe_allow_html=True)
                st.subheader(post['name'])
                col_v, col_t = st.columns(2)
                with col_v:
                    st.video(post['video_url'])
                with col_t:
                    st.write(post['lyrics'])
                    st.button(f"❤️ {post['likes']}", key=f"db_like_{post['id']}")
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Anslut Supabase för att se vad andra har skapat!")

st.markdown("<br><center><small>MAXIMUSIKAI // DATABASE EDITION</small></center>", unsafe_allow_html=True)





















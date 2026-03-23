import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="AI Director Studio", page_icon="🎬", layout="wide")

# LOGOTYP & STYLING
st.markdown("""
    <style>
    .logo-text {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 45px;
        font-weight: 800;
        background: -webkit-linear-gradient(#FF4B4B, #FF9B9B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .logo-sub {
        font-size: 14px;
        color: #808495;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# Visa Logotypen
st.markdown('<p class="logo-text">🎬 STUDIO TOMINGAI</p>', unsafe_allow_html=True)
st.markdown('<p class="logo-sub">POWERED BY MINIMAX AI</p>', unsafe_allow_html=True)

# Hämta API-nyckeln automatiskt från Streamlit Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

# --- Resten av din fungerande logik fortsätter här ---
if api_key_found:
    col1, col2 = st.columns(2)
    # ... (din befintliga kod för bild-uppladdning och regissörens val)






import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="TOMINGAI UNIVERSAL STUDIO", page_icon="🌐", layout="wide")

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
        font-family: 'Arial Black', sans-serif; font-size: 60px; font-weight: 900;
        color: #ffffff; text-transform: uppercase; letter-spacing: 5px;
        text-shadow: 0 0 10px #fff, 0 0 40px #00f2ff;
    }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing:10px;">UNIVERSAL TRANSLATOR ENGINE</p></div>', unsafe_allow_html=True)

# --- SIDOMENY: SPRÅK-MOTOR ---
with st.sidebar:
    st.header("🌐 Språk-Motor")
    input_lang = st.selectbox("Jag skriver på:", ["Svenska", "English", "Español", "Français", "日本語 (Japanese)", "Deutsch"])
    output_lang = st.selectbox("AI:n ska sjunga på:", ["English", "Svenska", "Español", "Français", "日本語 (Japanese)", "Italiano"])
    st.divider()
    st.info(f"Appen översätter från {input_lang} till {output_lang}!")

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Ditt manus")
        ide = st.text_area(f"Skriv din idé på {input_lang}:", f"En vacker natt under stjärnorna")
        stil = st.selectbox("Musikstil:", ["Pop", "Cyberpunk", "Jazz", "Epic"], key="m_stil")
    
    with col2:
        st.subheader("🎤 Sånginställning")
        magic_rost = st.radio("Sångröst:", ["Kvinna", "Man"], horizontal=True, key="m_voice")
        magic_speed = st.select_slider("Video-tempo:", options=["Slow Motion", "Normal", "Fast"])

    if st.button("🚀 PRODUCERA GLOBAL VIDEO"):
        with st.status(f"Översätter och producerar...") as status:
            try:
                # 1. Bild (FLUX)
                st.write("🎨 Skapar bild...")
                img_res = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{ide}, {stil} style, 4k", "aspect_ratio": "16:9"})
                st.image(img_res, caption="Genererad scen")
                
                # 2. Översättning (Llama)
                st.write(f"📝 Översätter från {input_lang} till {output_lang}...")
                lyrics_res = replicate.run("meta/meta-llama-3-70b-instruct", 
                    input={"prompt": f"The user wrote this in {input_lang}: '{ide}'. Translate it and write 4 short rhyming song lines in {output_lang}. ONLY return the lyrics."})
                final_lyr = "".join(lyrics_res).replace('"', '')

                # 3. Video & Musik (MiniMax)
                st.write(f"🎥 Genererar video ({magic_speed})...")
                v_url = str(replicate.run("minimax/video-01", input={"prompt": f"{magic_speed} cinematic movement", "first_frame_image": img_res}))
                
                st.write(f"🎵 Sjunger på {output_lang}...")
                m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{stil} style, {magic_rost} vocals", "lyrics": final_lyr}))

                # 4. Montering
                with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                clip = VideoFileClip("v.mp4")
                audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                
                st.video("out.mp4")
                st.success(f"Original: {ide} ➔ Sång ({output_lang}): {final_lyr}")
            except Exception as e: st.error(f"Fel: {e}")

else:
    st.error("Nyckel saknas i Secrets!")








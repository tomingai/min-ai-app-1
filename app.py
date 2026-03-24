import streamlit as st
import replicate
import os
import requests
import time
from moviepy.editor import VideoFileClip, AudioFileClip, vfx

# --- 1. GRUNDINSTÄLLNINGAR & DESIGN ---
st.set_page_config(page_title="TOMINGAI MEGA STUDIO", page_icon="⚡", layout="wide")

# Custom CSS för den ultimata neon-looken
st.markdown("""
    <style>
    .main { background-color: #050505; color: #fff; }
    .stApp { background-color: #050505; }
    .neon-container {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
        padding: 40px; border-radius: 20px; border: 2px solid #00f2ff;
        box-shadow: 0px 0px 40px rgba(0, 242, 255, 0.4);
        text-align: center; margin-bottom: 30px;
    }
    .neon-title { font-family: 'Arial Black', sans-serif; font-size: 65px; font-weight: 900; color: #fff; text-shadow: 0 0 20px #00f2ff; margin: 0; }
    .lyrics-box { background-color: #111; padding: 25px; border-radius: 15px; border-left: 5px solid #00f2ff; color: #eee; font-family: 'Courier New', monospace; margin-top: 20px; border: 1px solid #333; line-height: 1.6; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: black !important; font-weight: bold; }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; font-weight: bold; border-radius: 8px; height: 3.5em; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 25px #00f2ff; }
    .stSelectbox label, .stTextArea label, .stTextInput label, .stRadio label { color: #00f2ff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-container"><p class="neon-title">TOMINGAI</p><p style="color:#00f2ff; letter-spacing: 8px;">MEGA AI ENGINE // FULL EDITION</p></div>', unsafe_allow_html=True)

# HJÄLPFUNKTION FÖR ATT HANTERA REPLICATE-STRINGS
def get_url(output):
    if isinstance(output, list): return str(output[0])
    if hasattr(output, 'url'): return str(output.url)
    return str(output)

# --- 2. SIDOMENY (KONTROLLPANEL) ---
with st.sidebar:
    st.header("⚙️ MOTOR-INSTÄLLNINGAR")
    in_lang = st.selectbox("Ditt språk:", ["Svenska", "English", "Español", "日本語"])
    out_lang = st.selectbox("AI-språk (Sång/Text):", ["Svenska", "English", "Español", "Français", "日本語"])
    st.divider()
    m_voice = st.radio("Röstprofil:", ["Kvinna", "Man"])
    st.divider()
    st.warning("⚠️ Rate-limit skydd aktivt: Appen pausar 10s mellan steg för att undvika fel.")

# API-NYCKEL KOLL
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_ready = True
else:
    st.error("Gå till Streamlit Secrets och lägg till REPLICATE_API_TOKEN!")
    api_ready = False

# --- 3. HUVUDAPPEN ---
if api_ready:
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK"])

    # --- FLIK 1: TOTAL MAGI (GENERERA ALLT FRÅN TEXT) ---
    with tab1:
        col_m1, col_m2 = st.columns([1, 1.2])
        with col_m1:
            m_ide = st.text_area(f"Beskriv scenen ({in_lang}):", "En futuristisk stad i regn, neonljus speglas i asfalten", key="total_ide")
            m_stil = st.selectbox("Välj visuell stil:", ["Cyberpunk", "Cinematic", "Anime", "Vintage 8mm", "Abstract Art"], key="total_stil")
            if st.button("🚀 STARTA FULL PRODUKTION", key="total_btn"):
                with st.status("🎬 Bygger ditt mästerverk...", expanded=True) as status:
                    try:
                        # 1. BILD
                        status.write("🎨 Genererar grundbild...")
                        img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style, 16:9 aspect ratio", "aspect_ratio": "16:9"})
                        img_url = get_url(img_raw)
                        st.image(img_url, caption="Genererad Scen")
                        
                        status.write("⏳ Pausar för Rate Limit (10s)...")
                        time.sleep(10)

                        # 2. LYRICS
                        status.write("✍️ Skriver sångtext...")
                        lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 short rhyming lines in {out_lang} about: {m_ide}. No talk, ONLY lyrics.", "max_new_tokens": 100})
                        lyrics = "".join(lyrics_res).replace('"', '').strip()

                        status.write("⏳ Pausar för Rate Limit (10s)...")
                        time.sleep(10)

                        # 3. VIDEO
                        status.write("📽️ Animerar scenen...")
                        v_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement, high quality", "first_frame_image": img_url}))
                        
                        status.write("⏳ Sista pausen (10s)...")
                        time.sleep(10)

                        # 4. MUSIK
                        status.write("🎵 Komponerar musik...")
                        m_url = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": f"{m_stil} music, {m_voice} vocals, emotional", "duration": 10}))

                        # 5. MIXNING
                        status.write("🧪 Slutgiltig mixning i studion...")
                        with open("v_final.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a_final.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v_final.mp4")
                        audio = AudioFileClip("a_final.mp3")
                        
                        # Loopa video om ljudet är längre
                        if audio.duration > clip.duration:
                            clip = clip.fx(vfx.loop, duration=audio.duration)
                        else:
                            audio = audio.set_duration(clip.duration)
                        
                        clip.set_audio(audio).write_videofile("tomingai_output.mp4", codec="libx264", audio_codec="aac", logger=None)
                        
                        status.update(label="✅ PRODUKTION KLAR!", state="complete")
                        
                        with col_m2:
                            st.video("tomingai_output.mp4")
                            st.markdown(f'<div class="lyrics-box"><b>🎵 SÅNGTEXT ({out_lang}):</b><br><br>{lyrics.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
                            with open("tomingai_output.mp4", "rb") as f:
                                st.download_button("💾 LADDA NER VIDEO", f, "tomingai_video.mp4", "video/mp4")

                    except Exception as e:
                        st.error(f"Tekniskt fel: {e}")

    # --- FLIK 2: REGISSÖREN (BILD TILL VIDEO) ---
    with tab2:
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            bild_upload = st.file_uploader("Ladda upp en bild att animera", type=["jpg", "png", "jpeg"])
            if bild_upload: st.image(bild_upload, use_container_width=True)
        with col_r2:
            r_prompt = st.text_input("Beskriv rörelsen:", "Kameran rör sig långsamt framåt")
            if st.button("⚡ GENERERA VIDEO FRÅN BILD") and bild_upload:
                with st.spinner("Animerar..."):
                    # Notera: Minimax via Replicate kan ta filen direkt
                    v_res = get_url(replicate.run("minimax/video-01", input={"prompt": r_prompt, "first_frame_image": bild_upload}))
                    st.video(v_res)
                    st.success("Video genererad!")

    # --- FLIK 3: BARA MUSIK ---
    with tab3:
        col_mu1, col_mu2 = st.columns(2)
        with col_mu1:
            mu_prompt = st.text_area("Beskriv musiken:", "En lugn lo-fi beat med tunga basgångar")
            mu_dur = st.slider("Längd (sekunder):", 5, 20, 10)
        with col_mu2:
            if st.button("🎧 SKAPA ENDAST MUSIK"):
                with st.spinner("Komponerar..."):
                    mu_res = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": mu_prompt, "duration": mu_dur}))
                    st.audio(mu_res)
                    st.download_button("💾 LADDA NER MP3", requests.get(mu_res).content, "tomingai_audio.mp3")

# --- FOOTER ---
st.markdown("<br><hr><center><small>TOMINGAI MEGA ENGINE v2.0 | Powered by Replicate & Streamlit</small></center>", unsafe_allow_html=True)

















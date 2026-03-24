import streamlit as st
import replicate
import os
import requests
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

# HJÄLPFUNKTION FÖR ATT HÄMTA URL FRÅN REPLICATE-OBJEKT
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
    st.info("Tips: Beskriv stämningen noga i textrutan för bäst resultat.")

# Hämta API-nyckel från Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    st.error("⚠️ REPLICATE_API_TOKEN saknas i st.secrets!")
    api_key_found = False

if api_key_found:
    tab1, tab2, tab3 = st.tabs(["🪄 TOTAL MAGI", "🎬 REGISSÖREN", "🎧 BARA MUSIK"])

    # --- FLIK 1: TOTAL MAGI (AUTO-GENERING AV ALLT) ---
    with tab1:
        col1, col2 = st.columns([1, 1.2])
        with col1:
            m_ide = st.text_area(f"Vad ska filmen handla om? ({in_lang}):", "En ensam robot i ett neonbelyst regnigt Stockholm", key="m_ide")
            m_stil = st.selectbox("Visuell stil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Anime", "Oil Painting"], key="m_stil")
            m_btn = st.button("🚀 SKAPA FULLSTÄNDIG PRODUKT", key="m_btn")

        if m_btn:
            with st.status("🛠️ Startar studion...", expanded=True) as status:
                try:
                    # 1. Bild
                    status.write("🎨 Skapar den visuella världen...")
                    img_raw = replicate.run("black-forest-labs/flux-schnell", input={"prompt": f"{m_ide}, {m_stil} style, masterpiece, 16:9", "aspect_ratio": "16:9"})
                    img_url = get_url(img_raw)
                    
                    # 2. Text/Lyrics
                    status.write("✍️ Författar sångtext...")
                    lyrics_res = replicate.run("meta/llama-2-70b-chat", input={"prompt": f"Write 4 short rhyming lines in {out_lang} about '{m_ide}'. ONLY the lyrics, no talk.", "max_new_tokens": 100})
                    lyrics = "".join(lyrics_res).replace('"', '').strip()
                    
                    # 3. Video & Musik
                    status.write("📽️ Animerar scenen & 🎵 Komponerar musik...")
                    v_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic slow camera zoom", "first_frame_image": img_url}))
                    m_url = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": f"{m_stil} music, {m_voice} vocals, melodic", "duration": 10}))
                    
                    # 4. Mixning (MoviePy)
                    status.write("🧪 Mixar ljud och bild...")
                    with open("v1.mp4", "wb") as f: f.write(requests.get(v_url).content)
                    with open("a1.mp3", "wb") as f: f.write(requests.get(m_url).content)
                    
                    clip = VideoFileClip("v1.mp4")
                    audio = AudioFileClip("a1.mp3")
                    
                    # Loopa videon om musiken är längre
                    if audio.duration > clip.duration:
                        clip = clip.fx(vfx.loop, duration=audio.duration)
                    else:
                        audio = audio.set_duration(clip.duration)
                        
                    clip.set_audio(audio).write_videofile("out1.mp4", codec="libx264", audio_codec="aac", logger=None)
                    
                    status.update(label="✅ Produktion klar!", state="complete")
                    
                    with col2:
                        st.video("out1.mp4")
                        st.markdown(f'<div class="lyrics-box"><b>🎵 Sångtext ({out_lang}):</b><br><br>{lyrics.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
                        with open("out1.mp4", "rb") as file:
                            st.download_button("💾 LADDA NER VIDEO", file, "tomingai_master.mp4", "video/mp4")

                except Exception as e:
                    st.error(f"Ett tekniskt fel uppstod: {e}")

    # --- FLIK 2: REGISSÖREN (BILD TILL VIDEO) ---
    with tab2:
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            bild = st.file_uploader("Ladda upp en startbild (PNG/JPG)", type=["jpg", "png", "jpeg"])
            if bild: st.image(bild, caption="Din scen-förlaga", use_container_width=True)
        
        with col_r2:
            r_ide = st.text_input("Vad händer i scenen?", "En episk ballad om äventyr")
            if st.button("⚡ GENERERA FRÅN BILD") and bild:
                with st.status("🎬 Regisserar...") as status:
                    # Spara uppladdad bild tillfälligt för Replicate (måste ofta vara en URL, här skickas filen direkt)
                    # För enkelhets skull använder vi här samma flöde men med uppladdad fil
                    v_r_url = get_url(replicate.run("minimax/video-01", input={"prompt": "Cinematic movement", "first_frame_image": bild}))
                    m_r_url = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": f"Epic cinematic music, {m_voice} vocals", "duration": 8}))
                    
                    with open("v2.mp4", "wb") as f: f.write(requests.get(v_r_url).content)
                    with open("a2.mp3", "wb") as f: f.write(requests.get(m_r_url).content)
                    
                    clip2 = VideoFileClip("v2.mp4")
                    audio2 = AudioFileClip("a2.mp3").set_duration(clip2.duration)
                    clip2.set_audio(audio2).write_videofile("out2.mp4", codec="libx264", audio_codec="aac", logger=None)
                    
                    st.video("out2.mp4")
                    status.update(label="✅ Scenen är redo!", state="complete")

    # --- FLIK 3: BARA MUSIK ---
    with tab3:
        mus_col1, mus_col2 = st.columns(2)
        with mus_col1:
            mus_ide = st.text_area("Beskriv låtens tema:", "En hoppfull låt om en ny dag", key="mus_ide")
            mus_stil = st.text_input("Musikstil (t.ex. Lo-fi, Synthwave, Rock):", "Swedish Pop")
        
        with mus_col2:
            if st.button("🎵 GENERERA ENDAST LJUD"):
                with st.spinner("🎸 Komponerar..."):
                    mus_res = get_url(replicate.run("facebookresearch/musicgen", input={"prompt": f"{mus_stil}, {m_voice} vocals, {mus_ide}", "duration": 15}))
                    st.audio(mus_res)
                    st.download_button("💾 LADDA NER MP3", requests.get(mus_res).content, "tomingai_song.mp3")
                    st.success("Musiken är redo att laddas ner!")

else:
    st.warning("Vänligen konfigurera din Replicate API-nyckel i Streamlit Secrets för att starta motorn.")
















import streamlit as st
import replicate
import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="TOMINGAI NEON STUDIO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    .neon-wrapper {
        background-color: #0a0a0a; padding: 30px; border-radius: 15px;
        border: 1px solid #00f2ff; box-shadow: 0px 0px 20px #00f2ff;
        text-align: center; margin-bottom: 40px;
    }
    .neon-text {
        font-family: 'Courier New', Courier, monospace; font-size: 50px;
        font-weight: 900; color: #fff; text-shadow: 0 0 20px #00f2ff; margin: 0;
    }
    .stButton>button { background-color: transparent; color: #00f2ff; border: 2px solid #00f2ff; width: 100%; }
    .stButton>button:hover { background-color: #00f2ff; color: black; box-shadow: 0px 0px 15px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="neon-wrapper"><p class="neon-text">TOMINGAI</p><p style="color:#00f2ff;">A.I. VOICE & MOVIE ENGINE</p></div>', unsafe_allow_html=True)

if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
    api_key_found = True
else:
    api_key_found = False

if api_key_found:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📡 DATAKÄLLA: BILD")
        bild = st.file_uploader("Ladda upp bild", type=["jpg", "png", "jpeg"])
        if bild: 
            st.image(bild, use_container_width=True)
            if st.button("🪄 SKAPA MAGISK TEXT"):
                with st.spinner("AI:n skriver ren text..."):
                    try:
                        prompt = f"Skriv exakt 4 korta rimmade rader på svenska för en låt i stilen {st.session_state.get('stil_choice', 'Cyberpunk')}. Svara BARA med de 4 raderna, ingen annan text, inga rubriker, inga parenteser."
                        response = replicate.run(
                            "meta/meta-llama-3-70b-instruct",
                            input={
                                "prompt": prompt,
                                "system_prompt": "Du är en professionell låtskrivare. Du svarar ALDRIG med JSON eller metadata. Du svarar ENDAST med den rena svenska texten."
                            }
                        )
                        # Tvättar bort eventuellt skräp om AI:n ändå försöker med JSON
                        clean_text = "".join(response).replace('{', '').replace('}', '').replace('"lyrics":', '').replace('"', '').strip()
                        
                        st.session_state['ai_lyrics'] = clean_text
                        st.session_state['ai_v_prompt'] = "Slow cinematic zoom, high quality"
                        st.rerun()
                    except Exception as e:
                        st.error(f"AI-fel: {e}")

    with col2:
        st.subheader("🧠 PROCESSOR: RÖST & STIL")
        stil = st.selectbox("Filmstil:", ["Cyberpunk", "Vintage 8mm", "Cinematic", "Pop Art"], key="stil_choice")
        rost = st.radio("Välj röst som sjunger:", ["Kvinna (Female)", "Man (Male)"])
        
        v_prompt = st.text_input("Kamerarörelse:", st.session_state.get('ai_v_prompt', "Slow cinematic zoom"))
        lyrics = st.text_area("Låttext (Svenska):", st.session_state.get('ai_lyrics', "[Instrumental]"))
        
        if st.button("⚡ PRODUCERA MÄSTERVERK"):
            if not bild:
                st.error("Ladda upp en bild först!")
            else:
                with st.status("PROSESSERAR NEON-DATA...", expanded=True):
                    try:
                        # 1. Video (MiniMax)
                        st.write("🎥 Genererar video...")
                        v_url = str(replicate.run("minimax/video-01", input={"prompt": f"{v_prompt}, {stil} style", "first_frame_image": bild}))

                        # 2. Musik & Sång (MiniMax Music-1.5)
                        st.write("🎵 Genererar sång...")
                        m_url = str(replicate.run("minimax/music-1.5", input={"prompt": f"{stil} style, {rost} vocals, high quality", "lyrics": lyrics}))

                        # 3. Montering
                        with open("v.mp4", "wb") as f: f.write(requests.get(v_url).content)
                        with open("a.mp3", "wb") as f: f.write(requests.get(m_url).content)
                        
                        clip = VideoFileClip("v.mp4")
                        audio = AudioFileClip("a.mp3").set_duration(clip.duration)
                        clip.set_audio(audio).write_videofile("out.mp4", codec="libx264", audio_codec="aac")
                        
                        st.video("out.mp4")
                        with open("out.mp4", "rb") as f:
                            st.download_button("💾 EXPORTERA", f, "tomingai_master.mp4")
                    except Exception as e:
                        st.error(f"SYSTEMFEL: {e}")
else:
    st.error("⚠️ ÅTKOMST NEKAD: Kontrollera dina Secrets.")








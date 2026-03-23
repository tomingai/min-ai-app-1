import streamlit as st
import replicate
import os

# --- 1. DESIGN & LAYOUT ---
st.set_page_config(page_title="AI Studio Pro", page_icon="🎬", layout="wide")

# Custom CSS för att göra det snyggare (Dark Mode känsla)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF4B4B; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 AI Studio Pro")
st.markdown("Förvandla bilder till rörlig film med unik AI-musik.")

# --- 2. INSTÄLLNINGAR (SIDOMENY) ---
with st.sidebar:
    st.header("⚙️ Inställningar")
    api_key = st.text_input("Replicate API-nyckel:", type="password")
    st.info("Hämta din nyckel på ://replicate.com")

# --- 3. LOGIK & FUNKTIONER ---
if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📁 Ladda upp")
        bild = st.file_uploader("Välj en bild (JPG/PNG)", type=["jpg", "png", "jpeg"])
        if bild:
            st.image(bild, caption="Din originalbild", use_container_width=True)

    with col2:
        st.subheader("🎨 Kreativa val")
        v_prompt = st.text_input("Vad ska hända i videon?", "Cinematic movement, slow motion")
        m_prompt = st.text_input("Musikstil:", "Ambient, emotional, cinematic")
        
        generate_btn = st.button("🚀 STARTA GENERERING")

    if generate_btn and bild:
        with st.status("AI-magi pågår...", expanded=True) as status:
            try:
                # SKAPA VIDEO (MiniMax Video-01)
                st.write("🎥 Animerar bild med MiniMax...")
                video_output = replicate.run(
                    "minimax/video-01",
                    input={"prompt": v_prompt, "first_frame_image": bild}
                )
                video_url = str(video_output)
                st.video(video_url)
                
                # SKAPA MUSIK (AudioLDM)
                st.write("🎵 Komponerar musik...")
                music_output = replicate.run(
                    "cvssp/audioldm:b61392adec474775060c0ad3f71bc5a951458a5c97818b4e551f8aba3969139d",
                    input={"text": m_prompt, "duration": "10"}
                )
                music_url = str(music_output)
                st.audio(music_url)
                
                status.update(label="✨ Allt klart!", state="complete", expanded=False)
                st.success("Ditt mästerverk är redo!")

                # --- 4. LADDA NER ---
                st.subheader("💾 Spara resultatet")
                st.markdown(f"[Ladda ner Video]({video_url})")
                st.markdown(f"[Ladda ner Musik]({music_url})")

            except Exception as e:
                st.error(f"Något gick fel: {e}")
else:
    st.warning("👈 Klistra in din API-nyckel i sidomenyn för att börja!")




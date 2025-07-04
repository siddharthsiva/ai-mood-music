# ui.py

import streamlit as st

def apply_theme():
    st.set_page_config("AI Mood Music", layout="wide")
    st.markdown("""
    <style>
    html, body, .main, .block-container {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
    }

    h1, h2, h3, .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
        text-align: center;
    }

    .stButton > button {
        background-color: #1DB954 !important;
        color: white;
        padding: 12px 30px;
        border-radius: 30px;
        font-weight: bold;
        border: none;
        font-size: 16px;
    }

    .stButton > button:hover {
        background-color: #1ed760 !important;
    }

    .stSelectbox > div > div > div {
        background-color: #282828 !important;
        color: #ffffff !important;
        border-radius: 8px;
    }

    .muted {
        color: #aaaaaa;
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    @media (min-width: 768px) {
        .block-container {
            max-width: 700px;
            margin: auto;
            padding: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.image("https://cdn-icons-png.flaticon.com/512/0/375.png", width=60)
    st.markdown("# AI Mood Music 🎧", unsafe_allow_html=True)
    st.markdown('<p class="muted">Choose your mood. Let AI recommend the vibe.</p>', unsafe_allow_html=True)

def mood_selector():
    return st.selectbox("💬 How are you feeling today?", [
        "🎉 Happy", "😢 Sad", "🌙 Calm", "⚡ Energetic", "❤️ Romantic",
        "🧠 Focused", "🎭 Melancholy", "💪 Confident"
    ])

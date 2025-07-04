import streamlit as st
import json
from utils.storage import load_json, save_json

MOOD_HISTORY_FILE = "data/mood_history.json"

def log_mood(mood):
    history = load_json(MOOD_HISTORY_FILE)
    history.append({"mood": mood, "user": st.session_state.get("spotify_user", "anonymous")})
    save_json(MOOD_HISTORY_FILE, history)

def show_mood_history():
    history = load_json(MOOD_HISTORY_FILE)
    if history:
        st.markdown("### 📈 Your Mood History")
        for entry in reversed(history[-10:]):
            st.markdown(f"- {entry['user']} felt **{entry['mood']}**")
    else:
        st.markdown("No mood history yet.")

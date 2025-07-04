import streamlit as st
from utils.storage import load_json, save_json

FAV_FILE = "data/favorites.json"

def add_favorite(track_title):
    user = st.session_state.get("spotify_user", "anonymous")
    data = load_json(FAV_FILE)
    if user not in data:
        data[user] = []
    if track_title not in data[user]:
        data[user].append(track_title)
        save_json(FAV_FILE, data)

def show_favorites():
    user = st.session_state.get("spotify_user", "anonymous")
    data = load_json(FAV_FILE)
    st.markdown("### ⭐ Your Favorite Songs")
    for track in data.get(user, []):
        st.markdown(f"- {track}")

# app.py

import streamlit as st
from urllib.parse import parse_qs
from components.spotify_auth import get_auth_url, get_token, get_user_profile
from components.recommendations import get_song_recommendations
from components.mood_tracker import log_mood, show_mood_history
from components.favorites import add_favorite, show_favorites
from components.genre_tagging import tag_genre
from components.lyrics import display_lyrics
from components.playlist_editor import handle_playlist_creation
from components.collaboration import show_collab_info

st.set_page_config("AI Mood Music", layout="wide")
st.title("🎧 AI Mood Music")

# Mood input
mood = st.selectbox("How are you feeling today?", [
    "Happy", "Sad", "Calm", "Energetic", "Romantic", "Focused", "Melancholy", "Confident"
])

# Get song suggestions
if st.button("🔍 Get Song Recommendations"):
    log_mood(mood)
    st.session_state["tracks"] = get_song_recommendations(mood)

# Spotify login
if "spotify_token" not in st.session_state:
    query = st.query_params
    if "code" in query:
        tokens = get_token(query["code"])
        st.session_state["spotify_token"] = tokens["access_token"]
        st.session_state["spotify_user"] = get_user_profile(tokens["access_token"])["id"]
        st.rerun()
    else:
        st.markdown(f"[🔐 Log in with Spotify]({get_auth_url()})")
        st.stop()

token = st.session_state["spotify_token"]
user_id = st.session_state["spotify_user"]

# Show suggestions
if "tracks" in st.session_state:
    st.subheader(f"🎵 Songs for your {mood} mood:")
    for track in st.session_state["tracks"]:
        genre = tag_genre(track)
        st.markdown(f"- **{track}** (_{genre}_)")
        display_lyrics(track)
        if st.button(f"⭐ Favorite {track}", key=track):
            add_favorite(track)

    handle_playlist_creation(st.session_state["tracks"], token, user_id)

# Sidebar info
with st.sidebar:
    st.header("📈 Mood History")
    show_mood_history()
    st.header("🌟 Your Favorites")
    show_favorites()
    st.header("🤝 Collaboration")
    show_collab_info()

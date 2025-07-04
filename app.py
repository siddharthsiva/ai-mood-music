# app.py
import streamlit as st
from urllib.parse import urlparse, parse_qs
from spotify_api.auth import get_auth_url, get_token, get_user_profile
from spotify_api.tracks import search_track
from spotify_api.playlists import create_playlist, add_tracks_to_playlist, get_user_playlists, remove_track_from_playlist, rename_playlist
from gpt.gpt_recommender import get_songs_for_mood

st.set_page_config("AI Mood Music", layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
html, body, .main, .block-container {
    background-color: #000000 !important;
    color: #ffffff !important;
    font-family: 'Segoe UI', sans-serif;
}
.stButton > button {
    background-color: #1DB954 !important;
    color: white;
    font-weight: bold;
    border-radius: 30px;
    font-size: 16px;
    padding: 10px 25px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.image("https://cdn-icons-png.flaticon.com/512/0/375.png", width=64)
st.title("AI Mood Music 🎧")

mood = st.selectbox("How are you feeling today?", [
    "🎉 Happy", "😢 Sad", "🌙 Calm", "⚡ Energetic",
    "❤️ Romantic", "🧠 Focused", "🎭 Melancholy", "💪 Confident"
])

tracks = []
if st.button("🎧 Get Song Suggestions"):
    with st.spinner("Getting AI suggestions..."):
        gpt_songs = get_songs_for_mood(mood)
    st.subheader(f"Suggested Songs for {mood}")
    for s in gpt_songs:
        st.markdown(f"- {s}")
        tracks.append(s)

# --- Spotify Login ---
st.markdown("---")
if "spotify_token" not in st.session_state:
    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"]
        token_info = get_token(code)
        st.session_state["spotify_token"] = token_info["access_token"]
        st.rerun()
    else:
        st.markdown(f"<a href='{get_auth_url()}' style='color:#1DB954;'>🔓 Log in with Spotify</a>", unsafe_allow_html=True)
        st.stop()

token = st.session_state["spotify_token"]
profile = get_user_profile(token)
st.success(f"Logged in as: {profile['display_name']}")

# --- Playlist Management ---
user_playlists = get_user_playlists(token, profile["id"])
playlist_names = [pl["name"] for pl in user_playlists] + ["➕ Create New Playlist"]
selected_playlist = st.selectbox("Choose or Create a Playlist", playlist_names)

if selected_playlist == "➕ Create New Playlist":
    new_name = st.text_input("New Playlist Name")
    if st.button("Create Playlist") and new_name:
        playlist = create_playlist(token, profile["id"], new_name)
        selected_playlist = playlist["name"]
        st.success(f"Playlist '{new_name}' created!")
else:
    playlist_id = next((pl["id"] for pl in user_playlists if pl["name"] == selected_playlist), None)
    if st.button("✏️ Rename Playlist"):
        new_title = st.text_input("Enter new name")
        if new_title:
            rename_playlist(token, playlist_id, new_title)
            st.success(f"Renamed to {new_title}")

# --- Add Songs to Playlist ---
if tracks and selected_playlist:
    song_data = []
    for title in tracks:
        results = search_track(title, token)
        if results:
            song_data.append(results[0])
    for track in song_data:
        st.markdown(f"**{track['title']}** by *{track['artist']}*")
        st.markdown(f"[🔗 Spotify Link]({track['url']})")
        if track["preview"]:
            st.audio(track["preview"])
        if st.button(f"❌ Remove '{track['title']}' from Playlist"):
            remove_track_from_playlist(token, playlist_id, track["url"])
            st.rerun()

    if st.button("💾 Add to Playlist"):
        uris = ["spotify:track:" + track["url"].split("/")[-1] for track in song_data]
        add_tracks_to_playlist(token, playlist_id, uris)
        st.success("Tracks added!")

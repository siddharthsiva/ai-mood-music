import streamlit as st
from urllib.parse import urlparse, parse_qs
from spotify_api import get_auth_url, get_token, get_user_profile, search_track, create_playlist
from gpt_recommender import get_songs_for_mood
from playlist_manager import get_user_playlists, get_playlist_tracks, add_tracks_to_playlist, remove_track_from_playlist, update_playlist_details

st.set_page_config("AI Mood Music", layout="wide")

# --- Unified Theme + Custom Branding ---
st.markdown("""
<style>
html, body, .main, .block-container {
    background-color: #000000 !important;
    color: #ffffff !important;
    font-family: 'Segoe UI', sans-serif;
    padding: 0;
    margin: 0;
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

hr {
    border-top: 1px solid #333;
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

# --- Title and Custom Logo ---
st.image("https://cdn-icons-png.flaticon.com/512/0/375.png", width=60)  # Neutral play icon
st.markdown("# AI Mood Music 🎧", unsafe_allow_html=True)
st.markdown('<p class="muted">Choose your mood. Let AI recommend the vibe.</p>', unsafe_allow_html=True)

# --- Mood Selector ---
mood = st.selectbox("💬 How are you feeling today?", [
    "🎉 Happy", "😢 Sad", "🌙 Calm", "⚡ Energetic", "❤️ Romantic",
    "🧠 Focused", "🎭 Melancholy", "💪 Confident"
])

# --- GPT Song Suggestions ---
tracks = []
if st.button("🎧 Get My Song Suggestions"):
    with st.spinner("🤖 Asking AI for song ideas..."):
        gpt_songs = get_songs_for_mood(mood)
    st.markdown(f"## 🎵 AI picks for your {mood} mood:")
    for s in gpt_songs:
        st.markdown(f"- {s}")
        tracks.append(s)

# --- Spotify Login + Preview/Search ---
st.markdown("---")
st.markdown("## 🔓 Want to preview songs or save a playlist?", unsafe_allow_html=True)

# Handle redirect from Spotify
if "spotify_token" not in st.session_state:
    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"]
        token_info = get_token(code)
        st.session_state["spotify_token"] = token_info["access_token"]
        st.rerun()
    else:
        auth_url = get_auth_url()
        st.markdown(f"<a href='{auth_url}' style='color:#1DB954; font-weight:bold;'>🔒 Log in with Spotify to preview and save</a>", unsafe_allow_html=True)
        st.stop()

# --- After Login: Show Previews & Save ---
token = st.session_state["spotify_token"]
profile = get_user_profile(token)
st.success(f"✅ Logged in as: {profile['display_name']}")

if tracks:
    st.markdown("## ▶️ Preview Your Playlist")
    song_data = []
    for title in tracks:
        results = search_track(title, token)
        if results:
            song_data.append(results[0])

    for track in song_data:
        st.markdown(f"**{track['title']}** by *{track['artist']}*")
        st.markdown(f"[🔗 Listen on Spotify]({track['url']})")
        if track["preview"]:
            st.audio(track["preview"])
        st.markdown("---")

    if st.button("💾 Save Playlist to Spotify"):
        playlist = create_playlist(token, profile["id"], name=f"{mood} Mood Playlist")
        playlist_id = playlist["id"]
        track_uris = ["spotify:track:" + track["url"].split("/")[-1] for track in song_data]
        import requests
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, json={"uris": track_uris})
        st.success(f"✅ Playlist '{mood}' saved to your Spotify!")

# --- Playlist Management ---
st.markdown("---")
st.markdown("## 🎛️ Manage Your Playlists")

user_playlists = get_user_playlists(token)
playlist_options = {pl["name"]: pl["id"] for pl in user_playlists}

if playlist_options:
    selected_name = st.selectbox("🎵 Select one of your playlists", list(playlist_options.keys()))
    selected_id = playlist_options[selected_name]

    if st.checkbox("📂 Show tracks in playlist"):
        st.markdown("### Songs in Playlist:")
        tracks_in_pl = get_playlist_tracks(token, selected_id)
        for item in tracks_in_pl:
            track = item["track"]
            st.markdown(f"• {track['name']} by {track['artists'][0]['name']}")
            if st.button(f"🗑 Remove '{track['name']}'", key=track['id']):
                remove_track_from_playlist(token, selected_id, track["uri"])
                st.success(f"Removed {track['name']}")

    if tracks and st.button("➕ Add AI Mood Songs to Playlist"):
        uris = []
        for title in tracks:
            results = search_track(title, token)
            if results:
                uris.append("spotify:track:" + results[0]["url"].split("/")[-1])
        add_tracks_to_playlist(token, selected_id, uris)
        st.success(f"✅ Added {len(uris)} tracks to {selected_name}!")

    with st.expander("✏️ Rename Playlist"):
        new_name = st.text_input("New name", value=selected_name)
        new_desc = st.text_area("New description", "")
        if st.button("🔄 Update Playlist"):
            update_playlist_details(token, selected_id, new_name, new_desc)
            st.success("Playlist updated!")

import streamlit as st
import requests

def search_track(query, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 1}
    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    items = r.json().get("tracks", {}).get("items", [])
    return items[0] if items else None

def preview_tracks(track_list, token):
    st.markdown("## ▶️ Preview Your Playlist")
    st.session_state["track_uris"] = []
    for title in track_list:
        result = search_track(title, token)
        if result:
            uri = result["uri"]
            st.session_state["track_uris"].append(uri)
            st.markdown(f"**{result['name']}** by *{result['artists'][0]['name']}*")
            st.markdown(f"[🔗 Listen on Spotify]({result['external_urls']['spotify']})")
            if result["preview_url"]:
                st.audio(result["preview_url"])
            st.markdown("---")

def save_playlist_ui(track_list, token, profile, mood):
    name = st.text_input("Playlist name", f"{mood} Mood Playlist")
    description = st.text_area("Playlist description", "Created with AI Mood Music 🎧")
    public = st.checkbox("Make playlist public?", value=True)

    if st.button("💾 Save Playlist"):
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"name": name, "description": description, "public": public}
        res = requests.post(f"https://api.spotify.com/v1/users/{profile['id']}/playlists", headers=headers, json=payload)
        playlist = res.json()
        playlist_id = playlist["id"]
        requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, json={"uris": st.session_state["track_uris"]})
        st.success(f"✅ Playlist '{name}' created!")

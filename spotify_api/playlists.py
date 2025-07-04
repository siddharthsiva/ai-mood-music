import requests

def create_playlist(token, user_id, name, description="Created with AI Mood Music"):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"name": name, "description": description, "public": True}
    r = requests.post(f"https://api.spotify.com/v1/users/{user_id}/playlists", headers=headers, json=body)
    return r.json()

def get_user_playlists(token, user_id):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"https://api.spotify.com/v1/users/{user_id}/playlists", headers=headers)
    return r.json().get("items", [])

def add_tracks_to_playlist(token, playlist_id, uris):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, json={"uris": uris})

def remove_track_from_playlist(token, playlist_id, track_url):
    track_id = track_url.split("/")[-1]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"tracks": [{"uri": f"spotify:track:{track_id}"}]}
    requests.delete(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, json=payload)

def rename_playlist(token, playlist_id, new_name):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"name": new_name}
    requests.put(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers, json=payload)

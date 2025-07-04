import requests

def get_user_playlists(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    return r.json().get("items", [])

def get_playlist_tracks(token, playlist_id):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)
    return r.json().get("items", [])

def add_tracks_to_playlist(token, playlist_id, uris):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"uris": uris}
    ).json()

def remove_track_from_playlist(token, playlist_id, uri):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return requests.request("DELETE",
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"tracks": [{"uri": uri}]}
    ).json()

def update_playlist_details(token, playlist_id, name, description):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return requests.put(
        f"https://api.spotify.com/v1/playlists/{playlist_id}",
        headers=headers,
        json={"name": name, "description": description}
    ).json()

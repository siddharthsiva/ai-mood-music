import requests

def search_track(query, token, limit=1):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": limit}
    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    tracks = r.json().get("tracks", {}).get("items", [])
    return [
        {
            "title": t["name"],
            "artist": t["artists"][0]["name"],
            "url": t["external_urls"]["spotify"],
            "preview": t["preview_url"]
        } for t in tracks
    ]

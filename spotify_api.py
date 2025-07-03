# spotify_api.py
import base64
import requests
import streamlit as st
from urllib.parse import urlencode
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = "user-read-private playlist-modify-public"

def get_auth_url():
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": SCOPE
    }
    return f"{AUTH_URL}?{urlencode(params)}"

def get_token(code):
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }
    r = requests.post(TOKEN_URL, headers=headers, data=data)
    return r.json()

def get_user_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://api.spotify.com/v1/me", headers=headers)
    return r.json()

def search_track(query, token, limit=1):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": limit}
    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    results = r.json().get("tracks", {}).get("items", [])
    return [
        {
            "title": t["name"],
            "artist": t["artists"][0]["name"],
            "url": t["external_urls"]["spotify"],
            "preview": t["preview_url"]
        }
        for t in results
    ]

def create_playlist(token, user_id, name="AI Mood Playlist", description="Created with Streamlit + GPT"):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"name": name, "description": description, "public": True}
    r = requests.post(url, headers=headers, json=body)
    return r.json()

import streamlit as st
import requests
from urllib.parse import urlencode

SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = st.secrets["SPOTIFY_REDIRECT_URI"]

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = "playlist-modify-public user-read-private playlist-modify-private"

def get_auth_url():
    return f"{AUTH_URL}?{urlencode({'client_id': SPOTIFY_CLIENT_ID, 'response_type': 'code', 'redirect_uri': SPOTIFY_REDIRECT_URI, 'scope': SCOPE})}"

def get_token(code):
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    headers = {
        "Authorization": f"Basic {auth_str.encode('ascii').hex()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }
    return requests.post(TOKEN_URL, headers=headers, data=data).json()

def get_user_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get("https://api.spotify.com/v1/me", headers=headers).json()

def handle_auth_flow():
    params = st.query_params
    if "code" in params:
        code = params["code"]
        token_info = get_token(code)
        st.session_state["spotify_token"] = token_info["access_token"]
        st.rerun()
    else:
        st.markdown(f"<a href='{get_auth_url()}' style='color:#1DB954; font-weight:bold;'>🔒 Log in with Spotify</a>", unsafe_allow_html=True)

import requests

def fetch_lyrics(artist, title):
    try:
        res = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{title}")
        if res.status_code == 200:
            return res.json().get("lyrics", "Lyrics not found.")
        else:
            return "Lyrics not found."
    except:
        return "Lyrics API unavailable."

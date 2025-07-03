# 🎧 AI Mood-Based Spotify Recommender

This Streamlit app lets you log in with Spotify, describe your mood, and get a playlist generated using GPT + Spotify API.

## Features
- Spotify OAuth login
- GPT-powered mood-based music suggestions
- Song previews + Spotify links
- One-click playlist creation in your account

## Setup

1. Create a `.env` file or update `config.py` with:
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`
   - `OPENAI_API_KEY`
   - `SPOTIFY_REDIRECT_URI` (e.g., http://localhost:8501)

2. Install dependencies:
```bash
pip install -r requirements.txt

# 🎧 AI Mood Music

AI Mood Music is a full-featured, intelligent Spotify-connected web app that recommends music based on your current mood — and much more. Using GPT-powered suggestions and deep Spotify integration, users can generate playlists, tag songs by genre, fetch live lyrics, track mood history, and collaborate with friends. All in a clean, interactive UI powered by Streamlit.

---

## 🚀 Features

### 🧠 AI-Powered Song Recommendations
- Choose your current mood (Happy, Sad, Calm, etc.)
- Instantly receive 5 tailored song suggestions powered by GPT-4 or Claude.
- Real-time previews, metadata, and AI-generated genre tags.

### 🔐 Spotify Integration
- OAuth2 login with Spotify account.
- Create new playlists or edit existing ones.
- Add or remove tracks, update playlist names/descriptions.

### 🕒 Mood History Tracking
- Tracks daily moods and song choices.
- Visualize your emotional trends over time.

### ⭐ Favorite Songs
- Mark any recommended song as a favorite.
- Browse and revisit your curated favorites anytime.

### 🎼 Genre Tagging
- Each song is tagged with a suggested genre based on AI inference.
- Helps categorize songs for smarter playlists and filtering.

### 📖 Real-Time Lyrics
- Fetches lyrics for recommended tracks.
- Helpful for karaoke, language learning, or deeper song appreciation.

### 🤝 Collaborative Playlist Mode
- View and join public collaborative playlists.
- Combine moods from multiple users into shared playlists.

---
---

## 🛠️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/ai-mood-music.git
cd ai-mood-music


### 2. Install Dependencies
pip install -r requirements.txt

# 3. Add your API keys
#.streamlit/secrets.toml

SPOTIFY_CLIENT_ID = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8501"

OPENAI_API_KEY = "your_openai_api_key"         # Optional: for GPT-4
ANTHROPIC_API_KEY = "your_anthropic_api_key"   # Optional: for Claude

#4. Run the app
streamlit run app.py



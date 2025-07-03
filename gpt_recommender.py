# gpt_recommender.py
import streamlit as st
import anthropic

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

def get_songs_for_mood(mood):
    response = client.messages.create(
        model="claude-3-haiku-20240307",  # More stable & free-tier eligible
        max_tokens=300,
        temperature=0.7,
        system="You are a music recommendation assistant. Respond with only 5 numbered Spotify song titles with artists for a mood.",
        messages=[
            {
                "role": "user",
                "content": f"Give me 5 Spotify song titles and artists for a {mood.lower()} mood."
            }
        ]
    )

    raw = response.content[0].text
    return [line.strip("•- ") for line in raw.split("\n") if line.strip()]

# gpt_recommender.py
import anthropic
import streamlit as st

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"],
)

def get_songs_for_mood(mood):
    prompt = f"Give me 5 Spotify song titles and artist names for a {mood} mood."
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.content[0].text.strip()
    return [line.strip("-• ") for line in text.split("\n") if line.strip()]

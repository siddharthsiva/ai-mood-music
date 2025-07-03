# gpt_recommender.py
import anthropic
import streamlit as st

def get_songs_for_mood(mood):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    prompt = f"Suggest 5 popular Spotify songs for someone feeling {mood}. Respond with each line in format: Title - Artist"

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    text = response.content[0].text if response.content else ""
    return [line.strip() for line in text.split("\n") if "-" in line]

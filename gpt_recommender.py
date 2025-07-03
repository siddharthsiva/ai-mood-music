# gpt_recommender.py
import anthropic
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def get_songs_for_mood(mood):
    prompt = f"Suggest 5 popular Spotify songs for someone feeling {mood}. Respond with each line as: Title - Artist"
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",  # Or "claude-3-opus" if you're eligible
            max_tokens=300,
            temperature=0.8,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = response.content[0].text
        return [line.strip() for line in raw_text.split("\n") if " - " in line]
    except anthropic.APIError as e:
        return [f"Error getting songs: {e}"]

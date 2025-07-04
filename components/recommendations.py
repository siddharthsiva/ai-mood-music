import streamlit as st
import anthropic

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def get_songs_for_mood(mood):
    prompt = f"Suggest 5 song title and artist pairs for a {mood} mood. Format: Title - Artist"
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    lines = response.content[0].text.strip().split("\n")
    return [line.strip("-• ") for line in lines if line.strip()]

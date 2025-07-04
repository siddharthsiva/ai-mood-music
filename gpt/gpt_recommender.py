import streamlit as st
import anthropic

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def get_songs_for_mood(mood):
    prompt = f"""
Suggest 5 songs that match a {mood} mood.
Just list the song title and artist, no extra commentary.
Number them 1 to 5.
"""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",  # Or claude-3-haiku if preferred
        max_tokens=300,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse and clean results
    raw = response.content[0].text
    lines = raw.strip().split("\n")
    return [line.lstrip("12345. ").strip() for line in lines if line.strip()]

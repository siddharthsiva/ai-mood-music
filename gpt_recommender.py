import anthropic
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def get_songs_for_mood(mood):
    prompt = f"""
Suggest 5 Spotify songs that match a {mood} mood.
Respond in the format: Title - Artist.
Only list 5 songs. No explanation or commentary.
"""
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        temperature=0.8,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    text = response.content[0].text
    return [line.strip() for line in text.split("\n") if "-" in line]

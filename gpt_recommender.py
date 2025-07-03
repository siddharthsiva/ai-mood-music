# gpt_recommender.py
import streamlit as st
from anthropic import Anthropic

def get_songs_for_mood(mood):
    client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

    prompt = f"""Suggest 5 popular Spotify songs for someone feeling {mood}.
Respond with each line in the format: Title - Artist"""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        temperature=0.8,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Claude returns a list of content blocks
    content = response.content[0].text if response.content else ""
    return [line.strip() for line in content.split("\n") if "-" in line]

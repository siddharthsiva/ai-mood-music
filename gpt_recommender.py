# gpt_recommender.py
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import streamlit as st

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def get_songs_for_mood(mood):
    prompt = f"{HUMAN_PROMPT} Suggest 5 Spotify song titles and artist names for someone who feels {mood.lower()}.{AI_PROMPT}"

    response = client.completions.create(
        model="claude-2.1",  # Use a supported model like claude-2.1 if 3 isn't working
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )

    text = response.completion.strip()
    return [line.strip("-• ") for line in text.split("\n") if line.strip()]

from anthropic import Anthropic
import streamlit as st

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def get_songs_for_mood(mood):
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=500,
        temperature=0.7,
        messages=[
            {"role": "user", "content": f"Suggest 5 Spotify song titles for a {mood} mood. Just list them."}
        ]
    )
    return [line.strip("•- ") for line in response.content.split("\n") if line.strip()]

import streamlit as st
import anthropic

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

def get_songs_for_mood(mood):
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=400,
        temperature=0.7,
        system="You are a music recommendation expert.",
        messages=[
            {
                "role": "user",
                "content": f"Suggest 5 Spotify song titles that fit a {mood} mood. Respond with just the song titles, no explanation."
            }
        ]
    )
    # Clean up response
    raw = message.content[0].text
    return [line.strip("-• ") for line in raw.split("\n") if line.strip()]

import streamlit as st
import requests

# Title
st.title("🤖 Hugging Face Chat Assistant")

# Input box
user_input = st.text_input("You:", "")

# If user enters a message
if user_input:
    with st.spinner("Talking to assistant..."):
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}
        payload = {"inputs": {"text": user_input}}

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            generated_text = response.json()[0]["generated_text"]
            st.write("Assistant:", generated_text)
        else:
            st.error("Something went wrong. Try again later.")

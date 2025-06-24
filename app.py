import streamlit as st
import requests
import json

# ----------------------------
# App Setup
# ----------------------------
st.set_page_config(page_title="🌾 Farmer Assistant", page_icon="🌱")
st.title("🌱 Farmer Assistant – Your Smart Farming Buddy")
st.markdown("Ask about crops, weather, markets, diseases, or anything related to farming!")

# ----------------------------
# Hugging Face API Settings
# ----------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]  # Add this in Streamlit secrets
MODEL = "HuggingFaceH4/zephyr-7b-beta"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ----------------------------
# System Prompt
# ----------------------------
SYSTEM_PROMPT = """You are Farmer Assistant, an intelligent digital solution designed to empower farmers with real-time information, personalized guidance, and modern agricultural tools.

You help farmers make informed decisions, boost crop productivity, and manage their resources effectively. Whether it’s checking weather forecasts, diagnosing crop diseases, tracking market prices, or receiving seasonal farming tips, Farmer Assistant is your one-stop smart partner in the field.

Your tone is friendly, simple, and supportive. Always try to be practical, relevant to Indian agriculture, and concise.

Always follow this response format:
1. Answer clearly based on the question.
2. Give practical advice or steps when needed.
3. Use bullet points if listing tips or options.
4. End by asking: “Do you need help with anything else on your farm?”"""

# ----------------------------
# Chat State
# ----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ----------------------------
# HF Query Function
# ----------------------------
def query_zephyr(prompt):
    formatted = f"<|system|>\n{SYSTEM_PROMPT.strip()}\n<|user|>\n{prompt.strip()}\n<|assistant|>\n"
    payload = {
        "inputs": formatted,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result[0]["generated_text"].strip()
        elif response.status_code == 503:
            return "⏳ The model is still loading, try again in a few seconds."
        elif response.status_code == 401:
            return "🔒 Invalid or missing Hugging Face token."
        elif response.status_code == 402:
            return "❌ You’ve run out of HF inference credits. Use a smaller model or upgrade."
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"🚫 Failed to connect: {str(e)}"

# ----------------------------
# Chat Input
# ----------------------------
st.markdown("### 💬 Chat")
user_input = st.text_input("Ask your farming question", placeholder="e.g., Best fertilizer for tomato plants")

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        reply = query_zephyr(user_input)
        st.session_state.chat.append({"role": "user", "content": user_input})
        st.session_state.chat.append({"role": "assistant", "content": reply})
        #st.experimental_rerun()


# ----------------------------
# Show Chat History
# ----------------------------
for message in reversed(st.session_state.chat):
    with st.chat_message(message["role"]):
        st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown("Built with 🌿 using Zephyr 7B on Hugging Face Inference API")
st.markdown("Built By Edara Manikanta")

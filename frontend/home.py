import streamlit as st
import requests

# API endpoint of your FastAPI backend
BACKEND_URL = "https://sakura-speak.vercel.app/"

st.set_page_config(page_title="🌍 Text Translator", layout="centered")

st.title("🌍 Text Translator")
st.write("Translate text with automatic source language detection.")

# Text input
text_to_translate = st.text_area("Enter text to translate", height=150)

# Target language selection
target_lang = st.selectbox(
    "Select target language",
    ["English", "Hindi", "Spanish", "French", "German", "Japanese", "Chinese"]
)

if st.button("Translate"):
    if not text_to_translate.strip():
        st.warning("Please enter some text.")
    else:
        try:
            # Send request to backend
            files = {
                "text": (None, text_to_translate),
                "target_lang": (None, target_lang)
            }
            res = requests.post(BACKEND_URL, files=files)

            if res.status_code == 200:
                st.success("Translation Complete ✅")
                st.write("### Translated Text")
                st.markdown(f"```\n{res.text}\n```")
            else:
                st.error(f"Error {res.status_code}: {res.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

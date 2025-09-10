from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing; restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate/text")
async def translate_text(text: str = Form(...), target_lang: str = Form(...)):
    """
    Translate text to target language with automatic source language detection.
    """
    print("function called with", text, target_lang)

    model = "sonar-pro"  # Valid Perplexity model

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"You are a translation engine. Detect the source language automatically "
                    f"and translate ONLY the user's text into {target_lang}. For Example, if the user inputs India in english you will translate it to भारत in Hindi. No explanations or details, for India"
                    f"Return ONLY the translated text without explanations or extra formatting."
                )
            },
            {"role": "user", "content": text}
        ]
    }


    response = requests.post(url, json=payload, headers=headers)
    print("Response:", response.status_code, response.text)

    if response.status_code != 200:
        return f"Translation service error: {response.text}"

    try:
        translated = response.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Error parsing translation result."

    return translated.strip()

from mangum import Mangum
handler = Mangum(app)
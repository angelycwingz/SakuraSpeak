from fastapi import FastAPI, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
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
async def translate_text(text: str = Body(...), target_lang: str = Body(...)):
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
                    f"If user sends gibberish or non-language text, respond with 'Sorry! I can't translate gibberish.'"
                )
            },
            {"role": "user", "content": text}
        ]
    }


    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error from Perplexity API: {response.text}")

    try:
        translated = response.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Error parsing translation result."

    return translated.strip()
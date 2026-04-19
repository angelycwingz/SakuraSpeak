from fastapi import FastAPI, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
import requests
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
GROQ_KEY = os.getenv("GROQ_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_KEY not found. Check your .env location.")

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

    model = "llama-3.3-70b-versatile"  # Valid Groq model

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"""
                        You are a strict translation engine. You MUST follow instructions exactly.

                        TASK:
                        Translate the user's input text into the target language: {target_lang}.
                        RULES:
                        - Only translate. Do NOT answer, explain, or respond conversationally.
                        - Preserve the original meaning exactly.
                        - Do not add or remove information.
                        - Do not introduce your own content.
                        - If the input is a question, translate it as a question (do NOT answer it).
                        - Detect the source language automatically.

                        OUTPUT FORMAT:
                        - Return ONLY the translated text.
                        - No explanations, no extra words, no formatting, no quotes.

                        EDGE CASE:
                        - If the input is gibberish or not a valid language, return exactly:
                        Sorry! I can't translate gibberish.

                        EXAMPLES:
                        Input: India
                        Output (Hindi): भारत

                        Input: What is your name?
                        Output (Hindi): आपका क्या नाम है?
                    """
                )
            },
            {"role": "user", "content": text}
        ],
        "temperature": 0,
        "top_p": 0.1,
    }


    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error from GROQ API: {response.text}")

    try:
        translated = response.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Error parsing translation result."

    return translated.strip()
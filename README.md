# Language Translator App

A simple web-based language translator powered by FastAPI (backend) and Streamlit (frontend). The app uses Perplexity AI for translation with automatic source language detection.

## Features

- Translate text between multiple languages
- Automatic source language detection
- Clean, user-friendly interface
- FastAPI backend with CORS support
- Streamlit frontend for easy interaction

## Tech Stack

- FastAPI
- Uvicorn
- Streamlit
- Perplexity AI API
- Python-dotenv
- Requests

## Setup

1. **Clone the repository**

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Configure API Key**

   Add your Perplexity API key to `backend/.env`:

   ```
   PERPLEXITY_API_KEY=your_api_key_here
   ```

4. **Run the backend**

   ```sh
   uvicorn backend.main:app --reload
   ```

5. **Run the frontend**

   ```sh
   streamlit run frontend/home.py
   ```

## Usage

- Enter text to translate in the frontend.
- Select the target language.
- Click "Translate" to get the translated text.

## File Structure

```
.gitignore
requirements.txt
backend/
    .env
    main.py
frontend/
    home.py
```

##
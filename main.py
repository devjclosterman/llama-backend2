from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import openai
from datetime import datetime

load_dotenv()  # load environment variables from .env

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise Exception("OPENAI_API_KEY not set in environment")

app = FastAPI()

# Allow CORS from your frontend domain (change accordingly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://desertforgedai.local"],  # your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    client_id = data.get("client_id", "default_client")

    # Prepare the prompt or conversation context
    messages = [
        {"role": "system", "content": f"You are a helpful assistant for client {client_id}."},
        {"role": "user", "content": user_message}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    # Log the conversation
    with open("chat_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{datetime.now()}] Client: {client_id}\nUser: {user_message}\nBot: {bot_reply}\n\n")

    return {"reply": bot_reply}

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openai
import os
from typing import List, Dict

app = FastAPI(title="Azure GenAI Chatbot Playground")

# Allow CORS so you can test from local frontend or Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Azure OpenAI credentials from environment variables
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g. https://YOUR-RESOURCE.openai.azure.com/
openai.api_version = "2023-05-15"

# Keep conversation memory per session (simple in-memory dict)
conversations: Dict[str, List[Dict[str, str]]] = {}

@app.get("/")
def root():
    return {"message": "Welcome to your GenAI Chatbot Playground!"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")
    session_id = body.get("session_id", "default")  # default session if none provided

    if not user_input:
        return JSONResponse(status_code=400, content={"error": "No message provided."})

    # Initialize conversation history if new session
    if session_id not in conversations:
        conversations[session_id] = []

    # Append user message
    conversations[session_id].append({"role": "user", "content": user_input})

    try:
        # Call Azure OpenAI
        response = openai.ChatCompletion.create(
            engine="gpt-4",  # your deployment name in Azure
            messages=conversations[session_id],
            temperature=0.7,
            max_tokens=500
        )

        bot_reply = response['choices'][0]['message']['content']

        # Append bot reply to conversation history
        conversations[session_id].append({"role": "assistant", "content": bot_reply})

        return {"reply": bot_reply}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/reset")
async def reset_chat(request: Request):
    """Reset conversation for a session"""
    body = await request.json()
    session_id = body.get("session_id", "default")
    conversations[session_id] = []
    return {"message": f"Conversation for session '{session_id}' has been reset."}

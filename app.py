from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

# Load Azure OpenAI credentials from environment variables
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g. https://YOUR-RESOURCE.openai.azure.com/
openai.api_version = "2023-05-15"  # depends on your Azure OpenAI setup

@app.get("/")
def root():
    return {"message": "Hello, this is your GenAI chatbot running on Azure!"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")

    if not user_input:
        return {"error": "No message provided."}

    response = openai.ChatCompletion.create(
        engine="gpt-4",  # replace with your Azure deployment name
        messages=[{"role": "user", "content": user_input}]
    )

    return {"reply": response['choices'][0]['message']['content']}

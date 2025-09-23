import os
import openai
import gradio as gr
from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables
load_dotenv()

# Azure OpenAI credentials
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

# Configure Azure OpenAI
openai.api_type = "azure"
openai.api_base = OPENAI_ENDPOINT
openai.api_key = OPENAI_KEY
openai.api_version = "2023-05-15"

# Store chat history
conversations = {"gradio": []}

def gradio_chat(user_message, history):
    session_id = "gradio"
    conversations[session_id].append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        engine=OPENAI_DEPLOYMENT,
        messages=conversations[session_id],
        temperature=0.7,
        max_tokens=500,
    )

    bot_reply = response['choices'][0]['message']['content']
    conversations[session_id].append({"role": "assistant", "content": bot_reply})

    history.append((user_message, bot_reply))
    return history, ""

# Create Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Azure GenAI Chatbot Playground")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask me anything...")
    clear = gr.Button("Reset Chat")

    msg.submit(gradio_chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: ([], ""), None, [chatbot, msg], queue=False)

# Wrap in FastAPI for Azure
app = FastAPI()
app = gr.mount_gradio_app(app, demo, path="/")

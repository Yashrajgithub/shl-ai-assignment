from fastapi import FastAPI

from pydantic import BaseModel

from typing import List

from app.agent import generate_response


# -----------------------------
# FASTAPI INIT
# -----------------------------

app = FastAPI()


# -----------------------------
# ROOT + HEALTH ENDPOINT
# -----------------------------

@app.get("/")
@app.get("/health")
def home():

    return {
        "message": "SHL Conversational Assessment Recommender API is running",
        "docs": "/docs",
        "health": "/health"
    }


# -----------------------------
# REQUEST SCHEMA
# -----------------------------

class Message(BaseModel):

    role: str

    content: str


class ChatRequest(BaseModel):

    messages: List[Message]


# -----------------------------
# CHAT ENDPOINT
# -----------------------------

@app.post("/chat")

def chat(request: ChatRequest):

    messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in request.messages
    ]

    response = generate_response(messages)

    return response
from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()


class ChatRequest(BaseModel):
    query: str


@app.get("/")
def health_check():
    return {
        "status": "running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {
                "role": "user",
                "content": request.query
            }
        ]
    )

    return {
        "response": response["message"]["content"]
    }
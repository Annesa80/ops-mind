from fastapi import FastAPI
from pydantic import BaseModel

from backend.query import ask_opsmind

app = FastAPI()


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to OpsMind API"
    }


@app.post("/chat")
def chat(request: Question):

    return ask_opsmind(request.question)
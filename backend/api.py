from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi.responses import StreamingResponse
from backend.query import ask_opsmind_stream
# from backend.query import ask_opsmind

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to OpsMind API"
    }


# @app.post("/chat")
# def chat(request: Question):

#     return ask_opsmind(request.question)

@app.post("/chat")
def chat(request: Question):

    return StreamingResponse(
        ask_opsmind_stream(request.question),
        media_type="text/event-stream"
    )
import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from backend.query import ask_opsmind_stream
from backend.ingest import ingest_file


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


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# =====================
# Chat Models
# =====================

class Message(BaseModel):
    role: str
    content: str


class Question(BaseModel):
    messages: list[Message]


# =====================
# Routes
# =====================

@app.get("/")
def home():
    return {
        "message": "Welcome to OpsMind API"
    }


@app.post("/chat")
def chat(request: Question):

    return StreamingResponse(
        ask_opsmind_stream(request.messages),
        media_type="text/event-stream"
    )


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    file_id = str(uuid.uuid4())

    filename = (
        f"{file_id}_{file.filename}"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )


    # Save uploaded file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )


    try:

        chunks = ingest_file(filepath)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "chunks_added": chunks
        }


    except Exception as e:

        return {
            "error": str(e)
        }


    finally:

        if os.path.exists(filepath):
            os.remove(filepath)
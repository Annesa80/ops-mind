import os
import shutil
import uuid
import json

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.ingest import ingest_file

from backend.graph import graph

from dotenv import load_dotenv

load_dotenv(
    "C:/Users/Annesa/Desktop/OpsMind/.env",
    override=True,
)

import os


app = FastAPI()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# UPLOADS
# ============================================================

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


# ============================================================
# CHAT MODELS
# ============================================================

class ChatRequest(BaseModel):
    conversation_id: str
    question: str


# ============================================================
# ROUTES
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to OpsMind API"
    }


# ============================================================
# CHAT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.conversation_id
        }
    }

    def generate():

        for event in graph.stream(
            {
                "question": request.question,
            },
            config=config,
            stream_mode="custom",
        ):

            yield json.dumps(event) + "\n"

        yield json.dumps({
            "type": "done"
        }) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
    )


# ============================================================
# FILE UPLOAD
# ============================================================

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
        filename,
    )

    # --------------------------------------------------------
    # Save uploaded file
    # --------------------------------------------------------

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    try:

        chunks = ingest_file(
            filepath
        )

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "chunks_added": chunks,
        }

    except Exception as e:

        return {
            "error": str(e),
        }

    finally:

        if os.path.exists(filepath):

            os.remove(filepath)
# OpsMind

OpsMind is a Retrieval-Augmented Generation (RAG) chatbot for DevOps troubleshooting.

It uses a local knowledge base of Markdown files, retrieves relevant documentation using vector search, and generates answers with Ollama.

---

## Features

- 📄 Markdown knowledge base
- ✂️ Automatic document chunking
- 🔎 Semantic search with Qdrant
- 🤖 Local LLM using Ollama (Llama 3.2)
- 📚 Source citation for retrieved documents
- 🚫 "I don't know" guard when information is unavailable

---

## Tech Stack

- Python
- LangChain
- Ollama
- Qdrant
- Sentence Transformers
- HuggingFace Embeddings

---

## Project Structure

```
OpsMind/
│
├── backend/
│   ├── ingest.py
│   ├── llm.py
│   ├── main.py
│   ├── retriever.py
│   └── vectorstore.py
│
├── knowledge_base/
│   ├── docker_notes.md
│   ├── kubernetes_notes.md
│   ├── linux_errors.md
│   └── ...
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/OpsMind.git
cd OpsMind
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

Windows:

```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Start Qdrant

Run Qdrant using Docker.

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

## Start Ollama

Make sure Ollama is installed.

Pull the model.

```bash
ollama pull llama3.2
```

Start the Ollama server.

```bash
ollama serve
```

---

## Build the Vector Database

Run the ingestion script.

```bash
python backend/ingest.py
```

This will:

- Load Markdown documents
- Split them into chunks
- Generate embeddings
- Store them in Qdrant

---

## Run OpsMind

```bash
python backend/main.py
```

Example:

```
Ask OpsMind:
Why is my Kubernetes pod stuck in CrashLoopBackOff?
```

---

## Example Knowledge Base

- Docker
- Kubernetes
- Linux troubleshooting
- DevOps notes

---

## Future Improvements

- FastAPI backend
- Streamlit web interface
- Conversation memory
- Hybrid search
- Re-ranking
- PDF ingestion
- Multi-user support

---

## License

This project is for learning and educational purposes.
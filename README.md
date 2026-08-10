# OpsMind

**OpsMind is a Retrieval-Augmented Generation (RAG) chatbot for DevOps troubleshooting.**

It retrieves relevant troubleshooting knowledge from a local Markdown knowledge base and uses a local LLM through Ollama to generate grounded answers.

The retrieval pipeline combines **dense semantic search, BM25 keyword search, Reciprocal Rank Fusion (RRF), and BGE cross-encoder reranking** to improve retrieval quality while keeping the reranker conservative.

---

## ✨ Features

* 📄 Markdown-based DevOps knowledge base
* ✂️ Automatic document chunking
* 🔎 Dense semantic search with Qdrant
* 🔤 BM25 keyword retrieval
* 🔀 Hybrid retrieval using Reciprocal Rank Fusion (RRF)
* 🤖 BGE cross-encoder reranking
* 🧠 Local LLM inference with Ollama
* 💬 Conversation-aware streaming responses
* 📚 Source citation for retrieved documents
* 🚫 "I don't know" guard when relevant information is unavailable
* 📊 Retrieval evaluation with Recall@K and MRR
* 🧪 Regression analysis for comparing retrieval pipelines

---

## 🏗️ Retrieval Architecture

OpsMind uses a multi-stage retrieval pipeline:

```text
                    User Question
                          │
                          ▼
              ┌──────────────────────┐
              │   Hybrid Retrieval   │
              └──────────────────────┘
                    │          │
             ┌──────┘          └──────┐
             ▼                         ▼
      Dense Retrieval              BM25 Search
         Qdrant
             │                         │
             └──────────┬──────────────┘
                        ▼
              Reciprocal Rank Fusion
                        │
                        ▼
                Candidate Documents
                        │
                        ▼
              BGE Cross-Encoder
                 Reranking
                        │
                        ▼
              Top Relevant Context
                        │
                        ▼
                  Ollama LLM
                        │
                        ▼
                  Final Answer
```

### Why hybrid retrieval?

Dense retrieval is good at understanding semantic similarity, while BM25 is effective at matching exact technical terminology.

For example, a query containing:

```text
CrashLoopBackOff
```

may benefit from exact keyword matching, while a query such as:

```text
My container starts and then immediately dies
```

may benefit more from semantic retrieval.

RRF combines both retrieval signals before reranking.

### Why reranking?

The BGE cross-encoder evaluates the relationship between the user's question and each retrieved document more directly.

OpsMind uses BGE **conservatively** rather than allowing it to completely replace the RRF ranking.

The current approach gives RRF the primary influence while allowing BGE to improve the ordering of strong candidates.

```text
RRF        → primary ranking signal
BGE        → secondary relevance signal
```

This helps reduce cases where the reranker incorrectly moves a relevant document too far down the ranking.

---

## 📊 Retrieval Evaluation

OpsMind includes an evaluation pipeline for comparing different retrieval strategies.

The evaluation measures:

* **Recall@1**
* **Recall@3**
* **Recall@5**
* **MRR (Mean Reciprocal Rank)**
* BGE regressions compared with RRF

### Current evaluation

The retrieval system was evaluated against **46 test questions**.

| Pipeline      |  Recall@1 |  Recall@3 |  Recall@5 |       MRR |
| ------------- | --------: | --------: | --------: | --------: |
| Dense         |     0.783 |     0.935 |     0.957 |     0.857 |
| BM25          |     0.543 |     0.826 |     0.848 |     0.686 |
| RRF           |     0.804 |     0.870 |     0.913 |     0.853 |
| **RRF + BGE** | **0.804** | **0.913** | **0.957** | **0.861** |

The conservative BGE reranker improved:

* Recall@3: **0.870 → 0.913**
* Recall@5: **0.913 → 0.957**
* MRR: **0.853 → 0.861**

It also produced **0 observed regressions** against RRF in the current evaluation set.

The evaluation script is designed to make retrieval changes measurable rather than relying only on subjective testing.

---

## 🧰 Tech Stack

| Technology                | Purpose                       |
| ------------------------- | ----------------------------- |
| **Python**                | Application backend           |
| **LangChain**             | Retrieval and LLM integration |
| **Qdrant**                | Vector database               |
| **Sentence Transformers** | Embeddings and BGE reranking  |
| **BM25**                  | Keyword retrieval             |
| **Ollama**                | Local LLM inference           |
| **Llama 3.2**             | Local language model          |
| **Markdown**              | Knowledge base format         |

---

## 📁 Project Structure

```text
OpsMind/
│
├── backend/
│   ├── ingest.py
│   ├── llm.py
│   ├── main.py
│   ├── query.py
│   ├── retriever.py
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   ├── evaluate_retrieval.py
│   └── vectorstore.py
│
├── knowledge_base/
│   ├── docker_notes.md
│   ├── kubernetes_notes.md
│   ├── linux_errors.md
│   ├── redis_troubleshooting.md
│   └── ...
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/OpsMind.git
cd OpsMind
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Start Qdrant

OpsMind uses Qdrant as its vector database.

Run Qdrant with Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

## 🤖 Start Ollama

Install Ollama and pull the LLM:

```bash
ollama pull llama3.2
```

Start the Ollama server:

```bash
ollama serve
```

---

## 📚 Build the Knowledge Base

Run the ingestion pipeline:

```bash
python backend/ingest.py
```

The ingestion pipeline:

1. Loads Markdown documents
2. Splits documents into chunks
3. Generates embeddings
4. Stores vectors and metadata in Qdrant

---

## 🔎 Run OpsMind

Start the application:

```bash
python backend/main.py
```

Example question:

```text
Why is my Kubernetes pod stuck in CrashLoopBackOff?
```

OpsMind retrieves relevant troubleshooting documentation and uses the retrieved context to generate the answer.

---

## 🧪 Evaluate Retrieval

The project includes a retrieval evaluation dataset.

Run:

```bash
python backend/evaluate_retrieval.py
```

The evaluation compares:

```text
Dense
BM25
RRF
RRF + BGE
```

and reports:

```text
Recall@1
Recall@3
Recall@5
MRR
BGE regressions
```

This makes it possible to measure whether changes to the retrieval pipeline actually improve performance.

---

## 💡 Example

**Question**

```text
My container launches and then immediately dies. What could be wrong?
```

The retrieval pipeline may identify a relevant Docker troubleshooting chunk such as:

```text
Container keeps restarting

A Docker container repeatedly starts and stops.
This usually means the application inside the container is crashing.
```

The retrieved context is then passed to the local LLM to generate the final response.

---

## 🧠 Design Goals

OpsMind is designed around a few principles:

### Grounded answers

The LLM should answer using retrieved documentation rather than relying entirely on its internal knowledge.

### Local inference

The project uses Ollama so the LLM can run locally without requiring a hosted LLM API.

### Retrieval before generation

The quality of the retrieved context is treated as a separate engineering problem from LLM generation.

### Measurable improvements

Retrieval changes are evaluated using quantitative metrics instead of relying only on manual testing.

### Conservative reranking

The BGE reranker improves the RRF candidate ordering without being allowed to completely override the hybrid retrieval signal.

---

## 🚧 Future Improvements

Possible future improvements include:

* FastAPI API layer
* Web UI
* Persistent conversation memory
* Query rewriting
* Tool calling
* Agentic troubleshooting workflows
* PDF/document ingestion
* Metadata-aware filtering
* Retrieval caching
* Streaming API responses
* More comprehensive evaluation datasets
* Production monitoring and observability

---

## 🎯 Project Status

OpsMind currently has the core RAG retrieval pipeline implemented:

```text
Markdown Knowledge Base
        ↓
Document Chunking
        ↓
Dense Retrieval ──────┐
                      ├──→ RRF
BM25 Retrieval ───────┘
        ↓
BGE Reranking
        ↓
Relevant Context
        ↓
Ollama / Llama 3.2
        ↓
Grounded Response
```

The next stage of the project is to extend the RAG chatbot with **tool calling**, allowing OpsMind to move beyond documentation retrieval and perform useful DevOps actions through controlled tools.

---

## 📜 License

This project is for learning and educational purposes.

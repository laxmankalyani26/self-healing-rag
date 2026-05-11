# 🚀 Self-Healing Conversational RAG System

An enterprise-style Conversational Retrieval-Augmented Generation (RAG) system built using FastAPI, Streamlit, ChromaDB, Ollama, LangChain, and Docker.

This project enables users to upload PDF documents, perform semantic search over document content, and interact with an AI assistant capable of context-aware conversational question answering.

The system also includes self-healing retrieval logic that retries retrieval using rewritten queries when weak semantic matches are detected.

---

# ✨ Features

## 📄 PDF Document Ingestion

* Upload PDF documents dynamically
* Automatic text extraction and chunking
* Semantic embedding generation
* Persistent vector storage using ChromaDB

## 🧠 Conversational RAG

* Multi-turn conversational memory
* Context-aware retrieval
* Conversation history integration
* Natural AI chat experience

## 🔍 Semantic Search

* Vector similarity search using embeddings
* Top-k relevant chunk retrieval
* Source tracking with metadata

## 🛠 Self-Healing Retrieval Pipeline

* Confidence-based retrieval scoring
* Weak retrieval detection
* Automatic query rewriting
* Retry-based semantic recovery

## 🤖 Local LLM Integration

* Ollama-powered local inference
* Uses Phi-3 Mini model
* Low-latency local AI responses

## 🐳 Containerized Architecture

* Dockerized backend
* Dockerized frontend
* Docker Compose orchestration
* Multi-container networking

---

# 🏗️ System Architecture

```text
                    ┌────────────────────┐
                    │      User UI       │
                    │    (Streamlit)     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   FastAPI Backend  │
                    │  Conversational    │
                    │   RAG Pipeline     │
                    └─────────┬──────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
 ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
 │   ChromaDB     │  │ Embedding Model│  │     Ollama     │
 │ Vector Storage │  │ MiniLM-L6-v2  │  │   Phi3:Mini    │
 └────────────────┘  └────────────────┘  └────────────────┘
```

---

# ⚙️ Tech Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| Frontend         | Streamlit               |
| Backend          | FastAPI                 |
| Vector DB        | ChromaDB                |
| LLM              | Ollama (Phi3 Mini)      |
| Embeddings       | Sentence Transformers   |
| Framework        | LangChain               |
| Containerization | Docker + Docker Compose |
| Language         | Python                  |

---

# 🧠 How The System Works

## 1. PDF Upload

User uploads a PDF document through Streamlit UI.

## 2. Text Extraction & Chunking

The backend extracts document text and splits it into semantic chunks.

## 3. Embedding Generation

Each chunk is converted into vector embeddings using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

## 4. Vector Storage

Embeddings are stored persistently inside ChromaDB.

## 5. User Question

User asks a natural language question.

## 6. Conversational Retrieval

The system combines:

* recent conversation history
* current question

for context-aware semantic retrieval.

## 7. Confidence Evaluation

If retrieval confidence is weak:

* query rewriting activates
* retrieval retries automatically

## 8. LLM Response Generation

Retrieved context is passed to Ollama Phi-3 Mini model for grounded answer generation.

---

# 🔄 Self-Healing Retrieval Logic

The system includes an adaptive retrieval recovery pipeline.

### Workflow

```text
User Query
    ↓
Semantic Retrieval
    ↓
Confidence Check
    ↓
Weak Match?
    ↓ YES
Query Rewriting
    ↓
Retry Retrieval
    ↓
Generate Response
```

This improves:

* retrieval robustness
* ambiguous query handling
* conversational continuity

---

# 🐳 Dockerized Deployment

## Backend Container

* FastAPI API service
* Retrieval orchestration
* Vector search
* Ollama integration

## Frontend Container

* Streamlit UI
* Conversational interface
* PDF upload interface

## Docker Compose

Coordinates:

* frontend container
* backend container
* networking
* startup orchestration

---

# 🚀 Running The Project

## 1. Clone Repository

```bash
git clone <your-repository-url>
cd self-healing-rag
```

---

## 2. Start Ollama

```bash
ollama serve
```

Pull model:

```bash
ollama pull phi3:mini
```

---

## 3. Run Using Docker Compose

```bash
docker compose up --build
```

---

## 4. Access Application

Frontend:

```text
http://localhost:8501
```

Backend Docs:

```text
http://localhost:8000/docs
```

---

# 📂 Project Structure

```text
self-healing-rag/
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   ├── models/
│   │   ├── main.py
│   │   └── ...
│   ├── data/
│   ├── vectorstore/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# 📌 Key Engineering Concepts Demonstrated

* Conversational RAG
* Semantic Retrieval
* Vector Databases
* Self-Healing AI Pipelines
* Query Rewriting
* Confidence-Based Retrieval
* Docker Networking
* Multi-Container Architecture
* FastAPI Backend Design
* Local LLM Orchestration
* Persistent Vector Storage
* AI System Deployment

---

# 🔮 Future Enhancements

* Multi-document filtering
* Streaming responses
* Hybrid search (BM25 + Vector)
* Reranking pipeline
* Authentication system
* Cloud deployment
* Kubernetes orchestration
* CI/CD pipeline
* Multi-user support
* Role-based document isolation

---

#

---

# 👨‍💻 Author

Laxman Kalyani

AI Engineer | Generative AI | RAG Systems | FastAPI | LangChain | Docker

---

# ⭐ Project Highlights

✅ Conversational AI Assistant

✅ Self-Healing Retrieval Logic

✅ Fully Dockerized Architecture

✅ Persistent Vector Database

✅ Context-Aware Question Answering

✅ Enterprise-Style AI System Design

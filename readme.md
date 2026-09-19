# 🤖 Mini AI Knowledge Assistant

A local Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their contents.

The application retrieves relevant document sections using semantic search and generates grounded answers using a locally hosted Qwen3 8B model through Ollama.

---

## 🚀 Features

- PDF document upload
- Multiple document support
- PDF text extraction
- Automatic document chunking
- Semantic embeddings
- FAISS vector database
- Top-k similarity retrieval
- Local Qwen3 8B LLM
- Source/page citations
- Conversation history
- Streamlit web interface
- Local/private LLM inference

---

## 🏗️ Architecture

```text
                    PDF DOCUMENTS
                         │
                         ▼
                  ┌──────────────┐
                  │   PyMuPDF    │
                  │ Text Extract │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Chunking   │
                  │ 800 chars    │
                  │ 150 overlap  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Embeddings  │
                  │ MiniLM-L6-v2 │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │    FAISS     │
                  │ Vector Store │
                  └──────┬───────┘
                         │
                         │
                USER QUESTION
                         │
                         ▼
                  Query Embedding
                         │
                         ▼
                  FAISS Retrieval
                         │
                         ▼
                  Relevant Chunks
                         │
                         ▼
                  ┌──────────────┐
                  │   Qwen3 8B   │
                  │    Ollama    │
                  └──────┬───────┘
                         │
                         ▼
                       Answer
                         │
                         ▼
                  Source Citations

---


### 🔗 Project Links

**GitHub Repository:**  
https://github.com/AdityaKr6562/PDF-based-RAG-knowledge-assistant

**Live Demo:**  
Not deployed. The application currently runs locally using Streamlit and Ollama.

### 🧠 AI Tools Disclosure

AI tools were used during the development process for:

- Generating and refining code
- Improving documentation and README content
- Troubleshooting FAISS, embeddings and Streamlit integration

The final application was implemented, tested, and run locally by the developer.

### 🛠️ Development Tools

- Python 3.12
- VS Code
- Git / GitHub
- Streamlit
- PyMuPDF
- Sentence Transformers
- FAISS
- Ollama
- Qwen3 8B

### 🧪 Verification

The application was tested for:

- PDF text extraction
- Document chunking
- Embedding generation
- FAISS indexing
- Semantic retrieval
- RAG answer generation
- Source/page display
- Streamlit interface
- Conversation history

---
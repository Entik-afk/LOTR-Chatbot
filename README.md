# LOTR Book Oracle — RAG Chatbot

A Retrieval-Augmented Generation (RAG) system built over the full text of J.R.R. Tolkien's *The Lord of the Rings* trilogy. Ask anything about the books and get answers grounded directly in the source text.

---

## Features

- Vector database built from the three LOTR books
- CLI querying
- REST API via FastAPI
- Web UI served at `/`

---

## Project Structure

```
RAG/
├── data/                   # LOTR trilogy as .txt files
├── chroma_db/              # Persisted Chroma vector database
├── create_database.py      # Build and populate the vector DB
├── query_data.py           # Query via CLI
├── api.py                  # FastAPI server
├── index.html              # Web UI
├── .env                    # OpenAI API key (local only, not in git)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone & create virtual environment

```bash
git clone <your-repo-url>
cd RAG
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your OpenAI API key

Create a `.env` file:

```
OPENAI_API_KEY=sk-xxxx
```

---

## Usage

### Build the vector database

```bash
python create_database.py
```

This will:
- Load all `*.txt` files from `data/`
- Split text into chunks via `RecursiveCharacterTextSplitter`
- Generate embeddings using `text-embedding-3-large`
- Save the database to `chroma_db/`

> Only needs to be run once.

---

### Query via CLI

```bash
python query_data.py "Who is Aragorn?"
```

Output:

```
========= RESPONSE =========
Aragorn is...

========= SOURCES =========
* data/01 - The Fellowship Of The Ring.txt
* data/02 - The Two Towers.txt
```

---

### Run the API server

```bash
uvicorn api:app --reload
```

**Endpoint:** `POST /query`

Request:
```json
{
  "query": "Who is Gandalf?",
  "k": 10
}
```

Response:
```json
{
  "answer": "...",
  "sources": ["data/01 - The Fellowship Of The Ring.txt"],
  "chunks_used": 10
}
```

---

### Web UI

With the server running, open:

```
http://127.0.0.1:8000
```

Type your question and hit **Ask the Oracle**.

---

## How It Works

```
User question
     │
     ▼
ChromaDB similarity search  ──►  Top 10 relevant chunks
     │
     ▼
Prompt assembled with context
     │
     ▼
gpt-4o-mini generates answer
     │
     ▼
Answer + sources returned
```

---

## File Reference

| File | Description |
|------|-------------|
| `create_database.py` | Loads TXT files, chunks text, generates embeddings, saves to ChromaDB |
| `query_data.py` | CLI client — builds RAG prompt, calls ChatOpenAI, prints answer + sources |
| `api.py` | FastAPI server with `/query` endpoint and CORS enabled |
| `index.html` | JS frontend — sends query, displays answer and sources |

---

## Deploy to Render

1. Push the repo to GitHub (including `chroma_db/`)
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo
4. Set the following:

| Field | Value |
|-------|-------|
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn api:app --host 0.0.0.0 --port 10000` |

5. Add environment variable: `OPENAI_API_KEY` = your key
6. Click **Create Web Service**

Your app will be live at `https://your-app-name.onrender.com`

---

## Requirements

```
fastapi
uvicorn[standard]
python-dotenv
openai
langchain
langchain-openai
langchain-community
langchain-text-splitters
langchain-core
langchain-chroma
chromadb
```

import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ===== CONFIG =====
load_dotenv()
CHROMA_DB_PATH = "./chroma_db"

PROMPT_TEMPLATE = """Answer the question based ONLY on the following context:

{context}

---

Question: {question}

Answer:
"""


# ===== FASTAPI APP =====
app = FastAPI(title="RAG API", version="1.0")

# Jednou při startu aplikace, ne při každém requestu
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return FileResponse("index.html")

# ===== REQUEST MODEL =====
class QueryRequest(BaseModel):
    query: str
    k: int = 10


# ===== MAIN RAG ENDPOINT =====
@app.post("/query")
def query_rag(request: QueryRequest):
    query_text = request.query
    k = request.k



    # Retrieve relevant chunks
    results = db.similarity_search(query_text, k=k)

    if len(results) == 0:
        return {"answer": None, "sources": [], "message": "No context found"}

    # Build context
    context_text = "\n\n".join([doc.page_content for doc in results])

    # Build prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=context_text,
        question=query_text
    )

   
    response = model.invoke(prompt)

    # Sources
    source_docs = [doc.metadata.get("source", "unknown") for doc in results]

    return {
        "answer": response.content,
        "sources": source_docs,
        "chunks_used": len(results),
    }


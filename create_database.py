from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

import os
import shutil
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_PATH = "data/"
CHROMA_DB_PATH = "chroma_db/"


def main():
    create_database()


# --------------------------------------------------------
# LOAD ALL TXT DOCUMENTS
# --------------------------------------------------------

def load_documents():
    documents = []
    for root, dirs, files in os.walk("./data"):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                try:
                    # Nejprve UTF-8
                    loader = TextLoader(path, encoding="utf-8")
                    documents.extend(loader.load())
                except:
                    try:
                        # Zkus CP1250 (Windows)
                        loader = TextLoader(path, encoding="cp1250")
                        documents.extend(loader.load())
                    except:
                        try:
                            # Poslední možnost: otevři a ignoruj chyby
                            with open(path, "r", errors="ignore") as f:
                                text = f.read()
                                documents.append(Document(page_content=text, metadata={"source": path}))
                        except Exception as e:
                            print(f" Nelze načíst {path}: {e}")
                else:
                    print(f" Načteno {path}")
    return documents


# --------------------------------------------------------
# SPLIT INTO CHUNKS
# --------------------------------------------------------
def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        add_start_index=True,
    )

    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    # Only print preview if chunks exist
    if len(chunks) > 0:
        print("\n--- Example chunk ---")
        print(chunks[0].page_content)
        print(chunks[0].metadata)
    else:
        print(" WARNING: No chunks created!")

    return chunks


# --------------------------------------------------------
# SAVE TO CHROMA
# --------------------------------------------------------
def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    db.persist()

    print("Database created and saved to ChromaDB.")


# --------------------------------------------------------
# CREATE DATABASE PIPELINE
# --------------------------------------------------------
def create_database():
    documents = load_documents()

    if len(documents) == 0:
        print(" ERROR: No documents loaded. Check your ./data folder.")
        return

    chunks = split_text(documents)
    if len(chunks) == 0:
        print(" ERROR: No chunks generated. Stopping.")
        return

    save_to_chroma(chunks)


if __name__ == "__main__":
    main()

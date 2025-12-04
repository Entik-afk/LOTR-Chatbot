AG – Retrieval-Augmented Generation pro trilogii Pán Prstenů

Tento projekt implementuje kompletní RAG systém (Retrieval-Augmented Generation) nad texty trilogie Pán Prstenů od J. R. R. Tolkiena.
Systém umožňuje:

vytvořit vektorovou databázi z textových souborů

dotazovat se pomocí CLI

používat REST API

komunikovat přes jednoduché webové rozhraní (index.html)

📂 Struktura projektu
RAG/
│
├── data/                 # TXT soubory trilogie LOTR
├── chroma_db/            # Persistovaná Chroma vektorová DB
│
├── create_database.py    # Vytvoření a naplnění DB
├── query_data.py         # Dotazování přes CLI
├── api.py                # FastAPI server
├── index.html            # Webové UI
│
├── .env                  # API klíče pro OpenAI
└── README.md

⚙️ Instalace & spuštění
1️⃣ Klonování a příprava prostředí
git clone <repo>
cd RAG
python -m venv venv
source venv/bin/activate   # nebo venv\Scripts\activate na Windows
pip install -r requirements.txt

2️⃣ Přidej OpenAI API klíč

Vytvoř .env:

OPENAI_API_KEY=sk-xxxx

📥 1. Vytvoření vektorové databáze

Spusť:

python create_database.py


Skript:

načte všechny *.txt soubory z data/

rozdělí text do chunků

vytvoří embeddingy pomocí text-embedding-3-large

uloží je do chroma_db/

🔍 2. Dotazování přes CLI

Použití:

python query_data.py "Kdo je Aragorn?"


Skript:

načte databázi

vyhledá 10 nejrelevantnějších chunků

sestaví prompt

použije model gpt-4o-mini

vytiskne odpověď + seznam zdrojů

Ukázka výstupu:

========= RESPONSE =========
Aragorn je...

========= SOURCES =========
- data/lotr1.txt
- data/lotr2.txt

🌐 3. REST API (FastAPI)

Spuštění:

uvicorn api:app --reload

Endpoint: /query

POST JSON body:

{
  "query": "Kdo je Gandalf?",
  "k": 10
}


Odpověď:

{
  "answer": "...",
  "sources": ["data/lotr1.txt", "data/lotr3.txt"],
  "chunks_used": 10
}

💬 4. Webové rozhraní (index.html)

otevři index.html v prohlížeči

frontend se připojuje na http://127.0.0.1:8000/query

zadáš otázku, backend najde relevantní části knihy a vrátí odpověď

🧩 Popis jednotlivých souborů
🟦 create_database.py

načítá dokumenty (UTF-8 → CP1250 → fallback)

vytváří chunking přes RecursiveCharacterTextSplitter

generuje embeddingy (text-embedding-3-large)

ukládá databázi do ChromaDB

🟦 query_data.py

CLI klient pro dotazy

sestavuje RAG prompt

volá ChatOpenAI

vypisuje odpovědi + zdroje

🟦 api.py

FastAPI server

endpoint /query

CORS povoleno

používá stejnou RAG pipeline jako CLI

🟦 index.html

jednoduchý JavaScript frontend

odešle dotaz → zobrazí odpověď + použité zdroje

stylizace v čistém CSS

📦 Doporučený requirements.txt

Pokud ho chceš doplnit:

fastapi
uvicorn
python-dotenv
langchain
langchain-openai
langchain-community
langchain-text-splitters
langchain-core
langchain-chroma
openai
chromadb

🧪 Test funkčnosti

spusť FastAPI server:

uvicorn api:app --reload


otevři v prohlížeči:

http://127.0.0.1:8000


otevři index.html

zeptej se:

Kdo je Frodo?
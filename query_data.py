import argparse
import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


CHROMA_DB_PATH = "./chroma_db"

PROMPT_TEMPLATE = """Answer the question based ONLY on the following context:

{context}

---

Question: {question}

Answer:"""


def main():
    load_dotenv()

    # CLI argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query_text",
        type=str,
        help="The question to ask the vector database."
    )
    args = parser.parse_args()
    query_text = args.query_text

    # Load DB
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )

    # Search database
    results = db.similarity_search(query_text, k=10)

    if len(results) == 0:
        print("No relevant context found in the database.")
        return

    # Build context
    context_text = "\n\n".join([doc.page_content for doc in results])

    # Build prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=context_text,
        question=query_text
    )

    # Chat model
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)   # nebo jiný model
    response = model.invoke(prompt)

    # Extract sources
    source_docs = [doc.metadata.get("source", "unknown") for doc in results]

    # Final output
    print("\n========= RESPONSE =========")
    print(response.content)

    print("\n========= SOURCES =========")
    for src in source_docs:
        print("-", src)


if __name__ == "__main__":
    main()

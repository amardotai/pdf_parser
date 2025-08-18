# Assume `docs` is your list of Document objects
# from your example above

from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings

def doc_ingestion(docs):
    PG_CONN = "postgresql+psycopg://postgres:1234@localhost:5432/postgres"
    COLLECTION = "pdf_chunks"

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    vector_store = PGVector(
        connection=PG_CONN,
        collection_name=COLLECTION,
        embeddings=embeddings,
        use_jsonb=True
    )

    # Upsert them into pgvector
    ids = [f"chunk-{i}" for i in range(len(docs))]
    vector_store.add_documents(documents=docs, ids=ids)

    print("Inserted", len(ids), "chunks into pgvector.")

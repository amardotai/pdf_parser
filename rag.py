import psycopg
import json
from uuid import uuid4
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain.docstore.document import Document
from langchain_postgres import PGVector
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain.docstore.document import Document

def chunk_text(html):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    para_splits = md_splitter.split_text(html)
    header_splits = []
    headers = []
    for split in para_splits:
        flattened_header = " > ".join(split.metadata.values())
        if flattened_header not in headers:
            headers.append(flattened_header)
            header_doc = Document(page_content=flattened_header,metadata={"type":"header"})
            header_splits.append(header_doc)
        split.metadata["type"] = "para"
        split.metadata["flattened-header"] = flattened_header

    all_splits = header_splits+para_splits

    chunk_splitter = RecursiveCharacterTextSplitter(
        chunk_size=650,
        chunk_overlap=100,
        separators=["\n\n", ". ", "\n", ""]
    )

    docs = chunk_splitter.split_documents(all_splits)
    print("Chunking performed successfully")
    print(len(docs))

    return docs



PG_CONN = "postgresql+psycopg://postgres:1234@localhost:5432/postgres"
COLLECTION = "pdf_chunks"

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

vector_store = PGVector(
    connection=PG_CONN,
    collection_name=COLLECTION,
    embeddings=embeddings,
    use_jsonb=True,
    create_extension=False
)


llm = ChatOllama(model="mistral", temperature=0)
retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 3,"score_threshold":0.2})
def create_context(q: str):
    returned_docs = retriever.invoke(q)
    chunks = []

    for doc in returned_docs:
        if doc.metadata["type"] == "header":
            conn = psycopg.connect(
                "dbname=postgres user=postgres password=1234 host=localhost port=5432"
            )
            with conn.cursor() as cur:
                # Example: arbitrary SQL query on langchain_pg_embedding table
                cur.execute("""
                    SELECT document, cmetadata
                    FROM langchain_pg_embedding
                    WHERE cmetadata->>'flattened-header' = %s
                """,(doc.page_content,))
                rows = cur.fetchall()
            page_contents = [c.page_content for c in chunks]
            for document,cmetadata in rows:
                if document not in page_contents:
                    metadata = cmetadata if isinstance(cmetadata, dict) else json.loads(cmetadata)
                    chunks.append(Document(page_content=document, metadata=metadata))
        else:
            page_contents = [c.page_content for c in chunks]
            if doc.page_content not in page_contents:
                chunks.append(doc)
    return chunks




# Clears Collection before adding new pdf
def reset_collection(collection_name: str):
    conn = psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    with conn, conn.cursor() as cur:
        cur.execute("SELECT uuid FROM langchain_pg_collection WHERE name = %s", (collection_name,))
        row = cur.fetchone()
        if row:
            collection_id = row[0]
            print(f"🗑 Removing old collection '{collection_name}' ({collection_id})...")
            cur.execute("DELETE FROM langchain_pg_embedding WHERE collection_id = %s", (collection_id,))
            cur.execute("DELETE FROM langchain_pg_collection WHERE uuid = %s", (collection_id,))
        else:
            print(f"No existing collection named '{collection_name}' found.")



# Adds empty entry to create collection before
def ensure_collection_exists(collection_name):
    conn = psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    with conn, conn.cursor() as cur:
        # Check if collection exists
        cur.execute("SELECT uuid FROM langchain_pg_collection WHERE name = %s", (collection_name,))
        row = cur.fetchone()
        if not row:
            # Create collection manually
            collection_id = str(uuid4())
            cur.execute(
                "INSERT INTO langchain_pg_collection (uuid, name, cmetadata) VALUES (%s, %s, %s)",
                (collection_id, collection_name, "{}")
            )
            print(f"✅ Created collection '{collection_name}' with id {collection_id}")
        else:
            print(f"Collection '{collection_name}' already exists.")


def doc_ingestion(docs):
    reset_collection(COLLECTION)
    ensure_collection_exists(COLLECTION)
    ids = [f"chunk-{i}" for i in range(len(docs))]
    vector_store.add_documents(documents=docs, ids=ids)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the context below to answer. Answer only using the provided context. If the answer is not in the context, reply please question accordingly. Do not add extra text or instructions"),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

safe_question = RunnableLambda(lambda x: str(x["question"]) if isinstance(x, dict) else str(x))

rag_chain = (
    RunnableParallel({
        "docs": create_context,
        "question": safe_question
    })
    | RunnableParallel({
        "context": RunnableLambda(lambda x: format_docs(x["docs"])),
        "question": safe_question
    })
    | prompt
    | llm
    | StrOutputParser()
)

def ask(q: str):
    print("rag called")
    ret = create_context(q)
    with open("returned_chunks.txt","w",encoding='utf-8') as f:
        f.write("")

    for r in ret:
        with open("returned_chunks.txt","a",encoding='utf-8') as f:
            f.write("\n\n --- \n\n")
            f.write(r.page_content)
    return rag_chain.invoke(q)






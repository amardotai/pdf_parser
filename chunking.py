from langchain.text_splitter import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter


def chunk_text(html):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    header_splits = md_splitter.split_text(html)

    chunk_splitter = RecursiveCharacterTextSplitter(
        chunk_size=650,
        chunk_overlap=100,
        separators=["\n\n", ". ", "\n", ""]
    )

    docs = chunk_splitter.split_documents(header_splits)
    print("Chunking performed successfully")
    print(len(docs))

    return docs

from langchain.text_splitter import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter

def chunk_text(html):

    headers_to_split_on = [
        ("h1", "Header 1"),
        ("h2", "Header 2"),
    ]

    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    header_splits = html_splitter.split_text(html)

    chunk_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    docs = chunk_splitter.split_documents(header_splits)
    print("Chunking performed successfully")
    print(len(docs))
    return docs

from langchain.text_splitter import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter
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
    for split in para_splits:
        flattened_header = " > ".join(split.metadata.values())
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

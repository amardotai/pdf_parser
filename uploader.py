import streamlit as st
import ingestion
import pdf_processor
import chunking



file = st.file_uploader("Upload your pdf",type="pdf")

if file is not None:
    if st.button("Process"):
        html = pdf_processor.pdf_processor(file)
        chunked_doc = chunking.chunk_text(html)
        ingestion.doc_ingestion(chunked_doc)
        st.success("Documnet Ingested Successfully")
import streamlit as st
import rag
import pdf_processor
import chunking



file = st.file_uploader("Upload your pdf",type="pdf")

if file is not None:
    if st.button("Process"):
        html = pdf_processor.pdf_processor(file)
        chunked_doc = chunking.chunk_text(html)
        rag.doc_ingestion(chunked_doc)
        st.success("Documnet Ingested Successfully")
        st.session_state["doc_ingested"] = True

if st.session_state.get("doc_ingested"):
    question = st.text_input("Ask anything:")
    if st.button("Send"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            res = rag.ask(question)
            st.write(res)
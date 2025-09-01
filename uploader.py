import streamlit as st
import rag
import pdf_processor

file = st.file_uploader("Upload your pdf",type="pdf")

if file is not None:
    if st.button("Process"):
        md_parts = pdf_processor.pdf_processor(file)
        chunked_doc = rag.chunk_text(md_parts)
        rag.doc_ingestion(chunked_doc)
        st.success("Documnet Ingested Successfully")
        st.session_state["doc_ingested"] = True
        if "messages" in st.session_state:
            st.session_state.messages = []

if st.session_state.get("doc_ingested"):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if question := st.chat_input("Ask anything:"):
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})

        res = rag.ask(question)
        with st.chat_message("assistant"):
            st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
import streamlit as st
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_ollama.llms import OllamaLLM



# PDF Part



st.title("PDF QUERY TOOL")




# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def send_message():
    user_message = st.session_state.user_input
    if user_message.strip():
        st.session_state.messages.append(("user", user_message))
        reply = f"I received: {user_message}"
        st.session_state.messages.append(("bot", reply))
    st.session_state.user_input = ""  # safe here, inside callback

# Display chat history
for role, text in st.session_state.messages:
    st.markdown(f"**{role.capitalize()}:** {text}")

# Input widget with callback
st.text_input("Your message:", key="user_input", on_change=send_message)
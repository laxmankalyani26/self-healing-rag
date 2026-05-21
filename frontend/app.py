import streamlit as st
import requests
import os

# Backend URL
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://self-healing-rag-production.up.railway.app"
)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.title("Self-Healing RAG System")

# File Upload
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# Upload API Call
if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
        )
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files
        )

        if response.status_code == 200:

            st.success(
                response.json()["message"]
            )

        else:

            st.error(response.text)

    except Exception as e:

        st.error(f"Upload Error: {e}")

# Display Chat History
for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# Chat Input
query = st.chat_input(
    "Ask a question"
)

# Chat API Call
if query:

    st.session_state.chat_history.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):

        st.write(query)

    try:

        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "query": query,
                "chat_history": st.session_state.chat_history
            }
        )

        data = response.json()

        answer = data["answer"]

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):

            st.write(answer)

            st.subheader("Sources")

            for source in data["sources"]:

                st.write(source)

    except Exception as e:

        st.error(f"Chat Error: {e}")
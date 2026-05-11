import streamlit as st
import requests

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

st.title("Self-Healing RAG System")


uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
        )
    }

    response = requests.post(
        "http://backend:8000/upload",
        files=files
    )

    if response.status_code == 200:

        st.success(response.json()["message"])

    else:

        st.error(response.text)

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.write(message["content"])

query = st.chat_input(
    "Ask a question"
)


if query:

    st.session_state.chat_history.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):

        st.write(query)

    response = requests.post(
        "http://backend:8000/chat",
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
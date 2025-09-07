import streamlit as st
import requests

st.set_page_config(page_title="LangChain Gemini + LangGraph Chatbot", layout="wide")

st.title("LangChain Gemini + LangGraph Chatbot")

api_url = "http://localhost:8000"
user_id = "my_user"  # Use any unique value for demo

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []  # each entry: {"role": "user" or "assistant", "content": str}

def call_backend(message: str) -> str:
    try:
        response = requests.post(api_url + "/chat", json={"user_id": user_id, "message": message})
        if response.ok:
            return response.json().get("response", "No response from server.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept user input
user_input = st.chat_input("You:")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Optimistically show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get bot response from backend
    bot_response = call_backend(user_input)
    
    # Append and show bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

# File upload section (unchanged)
st.header("Upload and QA a Document")
file = st.file_uploader("Upload PDF or TXT")
if file:
    res = requests.post(f"{api_url}/upload", files={"file": file})
    st.write(res.json())
    question = st.text_input("Ask a question about the document:", key="file_question")
    if st.button("Ask Document QA") and question:
        resp = requests.post(f"{api_url}/ask_doc", data={"filename": file.name, "question": question})
        st.write("Bot:", resp.json()["response"])

# URL ingestion and QA section (unchanged)
st.header("Webpage RAG")
url = st.text_input("Enter a URL to index:", key="url_input")
if st.button("Index URL") and url:
    res = requests.post(f"{api_url}/index_url", data={"url": url})
    st.write(res.json())
url_q = st.text_input("Ask a question about the indexed URL:", key="url_question")
if st.button("Ask URL QA") and url and url_q:
    resp = requests.post(f"{api_url}/ask_url", data={"url": url, "question": url_q})
    try:
        resp_json = resp.json()
        bot_response = resp_json.get("response", "No response field in JSON.")
    except Exception as e:
        bot_response = f"Error decoding response: {e}\nRaw response:\n{resp.text}"

    st.write("Bot:", bot_response)

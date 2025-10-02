# LangChain Gemini + LangGraph Chatbot

This project is a chatbot application that uses a powerful combination of technologies to provide a conversational AI experience with Retrieval-Augmented Generation (RAG) capabilities.

## Features

*   **Conversational AI:** A stateful chatbot that can remember previous parts of the conversation.
*   **RAG on Documents:** Upload PDF or TXT documents and ask questions about their content.
*   **RAG on Web Pages:** Provide a URL and ask questions about the content of the web page.
*   **Powered by LangChain, LangGraph, and Gemini:** Built on a modern stack for building LLM applications.

## Technology Stack

*   **Backend:**
    *   [FastAPI](https://fastapi.tiangolo.com/): For creating the web server.
    *   [LangChain](https://www.langchain.com/): For building the core LLM logic.
    *   [LangGraph](https://langchain-ai.github.io/langgraph/): For creating a stateful, cyclical chatbot.
    *   [Google Gemini](https://deepmind.google/technologies/gemini/): The underlying language model.
    *   [Qdrant](https://qdrant.tech/): As an optional vector store for RAG.
*   **Frontend:**
    *   [Streamlit](https://streamlit.io/): For creating the user interface.

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── langgraph_workflow.py   # Defines the LangGraph chatbot
│   ├── rag_engine.py           # Handles RAG functionality
│   ├── chat_memory.py          # Manages conversational memory
│   ├── document_utils.py       # Utilities for handling documents
│   ├── url_utils.py            # Utilities for handling URLs
│   ├── vectorstore_manager.py  # Manages the vector store
│   └── schemas.py              # Pydantic schemas for API requests/responses
├── frontend/
│   └── app.py                  # Streamlit frontend application
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Getting Started

### Prerequisites

*   Python 3.7+
*   A Google API key with the Gemini API enabled.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd langgraph_chatbot
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root of the project and add your Google API key:
    ```
    GOOGLE_API_KEY="your-google-api-key"
    ```

### Running the Application

1.  **Start the backend server:**
    ```bash
    uvicorn backend.main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

2.  **Start the frontend application:**
    In a new terminal, run:
    ```bash
    streamlit run frontend/app.py
    ```
    The frontend will be accessible at `http://localhost:8501`.

## How to Use

1.  **Chat:**
    *   Open the Streamlit app in your browser.
    *   Use the chat input at the bottom of the page to have a conversation with the chatbot.

2.  **Document Q&A:**
    *   Use the "Upload and QA a Document" section to upload a PDF or TXT file.
    *   Once the file is uploaded, enter a question in the text input and click "Ask Document QA".

3.  **Web Page Q&A:**
    *   Use the "Webpage RAG" section to enter a URL.
    *   Click "Index URL" to have the chatbot process the web page.
    *   Enter a question in the text input and click "Ask URL QA".

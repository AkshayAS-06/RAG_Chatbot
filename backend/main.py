from fastapi import FastAPI, UploadFile, File, Form
from backend.schemas import ChatRequest, ChatResponse
from backend.chat_memory import chat_with_langgraph_memory
from backend.document_utils import save_uploaded_file, extract_text_from_file
from backend.rag_engine import ingest_and_index, query_document
from backend.url_utils import index_url, ask_url

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    result = await chat_with_langgraph_memory(req.user_id, req.message)
    return ChatResponse(**result)

@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    filepath = await save_uploaded_file(file)
    text = extract_text_from_file(filepath)
    ingest_and_index(file.filename, text)
    return {"filename": file.filename, "status": "uploaded"}

@app.post("/ask_doc")
async def ask_doc(filename: str = Form(...), question: str = Form(...)):
    resp = query_document(filename, question)
    return {"response": resp}

@app.post("/index_url")
async def index_url_endpoint(url: str = Form(...)):
    await index_url(url)
    return {"status": "URL indexed"}

@app.post("/ask_url")
async def ask_url_endpoint(url: str = Form(...), question: str = Form(...)):
    resp = await ask_url(url, question)
    return {"response": resp}

import os
import aiofiles
from PyPDF2 import PdfReader
from backend.config import UPLOAD_DIR

async def save_uploaded_file(file):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(filepath, "wb") as out_file:
        await out_file.write(await file.read())
    return filepath

def extract_text_from_file(filepath):
    text = ''
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        text = " ".join([p.extract_text() or "" for p in reader.pages])
    elif filepath.endswith(".txt"):
        with open(filepath, "r") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format.")
    return text

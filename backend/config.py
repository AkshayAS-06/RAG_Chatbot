import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../uploaded_docs"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

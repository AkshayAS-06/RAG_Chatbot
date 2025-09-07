from langchain_qdrant import QdrantVectorStore
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from backend.config import QDRANT_URL, QDRANT_API_KEY  # add API key if used

stores = {}

def get_embedding_fn():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Initialize Qdrant client once
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY if 'QDRANT_API_KEY' in globals() else None,
    prefer_grpc=False,
)

def build_or_get_store(name, texts, use_qdrant=False):
    embeddings = get_embedding_fn()
    if use_qdrant:
        # Create collection if not exists
        try:
            qdrant_client.get_collection(name)
        except Exception:
            qdrant_client.recreate_collection(
                collection_name=name,
                vectors_config=VectorParams(size=embeddings.get_embedding_dim(), distance=Distance.COSINE)
            )

        # Build vector store by embedding texts and storing in Qdrant
        store = QdrantVectorStore.from_texts(
            texts,
            embedding=embeddings,
            client=qdrant_client,
            collection_name=name
        )
    else:
        store = InMemoryVectorStore.from_texts(texts, embedding=embeddings)
    # Cache in-memory for session
    stores[name] = store
    return store

def get_store(name):
    # Return cached vector store instance if exists
    if name in stores:
        return stores[name]
    # Try loading existing Qdrant collection as vectorstore
    try:
        embeddings = get_embedding_fn()
        store = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            client=qdrant_client,
            collection_name=name,
        )
        stores[name] = store
        return store
    except Exception:
        return None

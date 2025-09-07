from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.vectorstore_manager import build_or_get_store, get_store

def ingest_and_index(filename, text, use_qdrant=False):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    return build_or_get_store(filename, chunks, use_qdrant=use_qdrant)

def query_document(filename, question):
    vecstore = get_store(filename)
    if not vecstore:
        print("No vector store found for:", filename)
        return "Document is not ingested yet."

    results = vecstore.similarity_search(question)
    if results and len(results) > 0:
        print(f"Found {len(results)} results for question: {question}")
        for i, doc in enumerate(results):
            print(f"Result {i+1}:")
            print(f"Content: {doc.page_content[:500]}")  # print first 500 chars
            print(f"Metadata: {doc.metadata}")
            print("-----")
        return results[0].page_content  # Return first matched chunk
    else:
        print("No results found for question:", question)
        return "Nothing found."


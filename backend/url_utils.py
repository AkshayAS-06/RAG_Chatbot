import requests
from backend.rag_engine import ingest_and_index, query_document
from bs4 import BeautifulSoup

def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    # Remove style and script tags
    for tag in soup(["style", "script", "noscript"]):
        tag.decompose()
    paragraphs = soup.find_all("p")
    cleaned_text = "\n\n".join([p.get_text() for p in paragraphs if p.get_text(strip=True)])
    return cleaned_text

async def index_url(url, use_qdrant=False):
    print(f"Fetching URL: {url}")
    headers = {"User-Agent": "LangGraphBot/1.0 (your-email@example.com)"}
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        raw_html = response.text
        print(f"Fetched {len(raw_html)} characters of HTML")

        cleaned_text = clean_html(raw_html)
        print(f"Cleaned text length: {len(cleaned_text)} characters")
        
        # Print a snippet of the cleaned text for verification
        print(f"Sample cleaned text:\n{cleaned_text[:1000]}")  # print first 1000 characters
        
        ingest_and_index(url, cleaned_text, use_qdrant=use_qdrant)
        print("Data ingestion completed")
        return {"status": "URL indexed successfully"}
    else:
        print(f"Failed to fetch URL: {response.status_code}")
        return {"status": f"Failed to fetch URL: {response.status_code}"}



async def ask_url(url, question):
    print(f"Querying indexed data for URL: {url} with question: {question}")
    answer = query_document(url, question)
    print(f"Query result: {answer}")
    return answer


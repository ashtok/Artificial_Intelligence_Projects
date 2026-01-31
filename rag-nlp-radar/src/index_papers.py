# src/index_papers.py
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

RAW_DIR = Path("data/raw")
DB_DIR = Path("data/db")
DB_DIR.mkdir(parents=True, exist_ok=True)

def load_latest_metadata():
    files = sorted(RAW_DIR.glob("nlp_papers_*.json"))
    if not files:
        raise ValueError("No papers found. Run fetch_papers first!")
    latest = files[-1]
    return json.loads(latest.read_text(encoding="utf-8"))

def build_index():
    papers = load_latest_metadata()
    print(f"Indexing {len(papers)} papers...")
    
    texts = []
    metadatas = []
    
    for p in papers:
        text = f"Title: {p['title']}\n\nAbstract: {p['abstract']}"
        texts.append(text)
        metadatas.append({
            "arxiv_id": p["arxiv_id"],
            "title": p["title"][:100] + "..." if len(p["title"]) > 100 else p["title"],
            "published": p["published"],
            "pdf_url": p["pdf_url"],
        })
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.create_documents(texts, metadatas=metadatas)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(
        docs, embeddings, persist_directory=str(DB_DIR)
    )
    vectordb.persist()
    print(f"✅ Indexed {len(papers)} papers into Chroma DB")

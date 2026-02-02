# src/rag_agent.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathlib import Path

DB_DIR = Path("data/db")

SUMMARY_PROMPT = """
You are an expert NLP researcher.

Summarize this paper using EXACTLY this format:

- Problem:
- Method: 
- Data:
- Key results:
- Limitations:
- When to read full paper:

Paper: {context}
"""

def get_vectordb():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(
        embedding_function=embeddings,
        persist_directory=str(DB_DIR)
    )

def summarize_by_id(arxiv_id: str):
    vectordb = get_vectordb()
    docs = vectordb.similarity_search(arxiv_id, k=1)
    if not docs:
        return f"No paper found with ID: {arxiv_id}"
    
    doc = docs[0]
    context = doc.page_content
    # For now, return raw formatted text (add LLM later)
    return f"""
{doc.metadata.get('title', 'No title')}
arxiv.org/abs/{doc.metadata.get('arxiv_id', 'unknown')}

Raw abstract for manual review:
{context[:1000]}..."""

def summarize_latest(n: int = 5):
    vectordb = get_vectordb()
    # Get most recent by similarity to "NLP" (will improve later)
    docs = vectordb.similarity_search("NLP research paper", k=n)
    results = []
    
    for i, doc in enumerate(docs):
        results.append((
            doc.metadata.get("arxiv_id", f"paper_{i}"),
            doc.metadata.get("title", "No title"),
            doc.page_content[:500] + "..."  # Truncated for now
        ))
    return results

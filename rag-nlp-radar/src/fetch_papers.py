import arxiv
from datetime import datetime, timedelta
import json
from pathlib import Path

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_latest_nlp(max_results: int = 50):
    query = "cat:cs.CL OR cat:cs.LG OR cat:cs.AI"
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )  # [web:50][web:51]

    papers = []
    for r in search.results():
        papers.append({
            "id": r.entry_id,
            "arxiv_id": r.get_short_id(),
            "title": r.title,
            "abstract": r.summary,
            "authors": [a.name for a in r.authors],
            "published": r.published.isoformat(),
            "updated": r.updated.isoformat(),
            "pdf_url": r.pdf_url,
            "primary_category": r.primary_category,
            "categories": list(r.categories),
        })

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = DATA_DIR / f"nlp_papers_{ts}.json"
    out_path.write_text(json.dumps(papers, indent=2), encoding="utf-8")
    return papers

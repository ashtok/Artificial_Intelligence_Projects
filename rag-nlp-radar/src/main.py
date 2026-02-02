# src/main.py
import argparse
from fetch_papers import fetch_latest_nlp
from index_papers import build_index
from rag_agent import summarize_by_id, summarize_latest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update",
        action="store_true",
        help="Fetch latest papers and rebuild index",
    )
    parser.add_argument(
        "--summarise-id",
        type=str,
        help="arXiv ID to summarise",
    )
    parser.add_argument(
        "--summarise-latest",
        type=int,
        help="Summarise latest N papers",
    )
    parser.add_argument(
        "--test-run",
        action="store_true",
        help="Do a small end-to-end test (fetch, index, summarise 1 paper)",
    )
    args = parser.parse_args()

    # Full update
    if args.update:
        fetch_latest_nlp()
        build_index()

    # Normal flows
    if args.summarise_id:
        print(summarize_by_id(args.summarise_id))

    if args.summarise_latest:
        for arxiv_id, title, summary in summarize_latest(args.summarise_latest):
            print("=" * 80)
            print(f"{arxiv_id} — {title}")
            print(summary)
            print()

    # Test run: minimal end‑to‑end smoke test
    if args.test_run:
        print("[TEST] Fetching a few latest NLP papers...")
        fetch_latest_nlp(max_results=3)
        print("[TEST] Building index...")
        build_index()
        print("[TEST] Summarising 1 paper from the latest batch...")
        results = summarize_latest(1)
        for arxiv_id, title, summary in results:
            print("=" * 80)
            print(f"[TEST] {arxiv_id} — {title}")
            print(summary)
            print()
        print("[TEST] Done. If you see a summary above, the basic pipeline works.")


if __name__ == "__main__":
    main()

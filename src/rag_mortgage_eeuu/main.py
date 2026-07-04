"""CLI entry points for the RAG mortgage knowledge base."""

import argparse

from dotenv import load_dotenv

from rag_mortgage_eeuu.ingest import ingest


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="RAG Mortgage EEUU")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest", help="Ingest PDFs into the knowledge base")
    ingest_parser.add_argument(
        "--no-clear", action="store_true", help="Skip clearing the index"
    )

    args = parser.parse_args()

    if args.command == "ingest":
        count = ingest(clear=not args.no_clear)
        print(f"Ingested {count} chunks from PDFs into the knowledge base.")


if __name__ == "__main__":
    main()

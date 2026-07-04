import time
from pathlib import Path
from typing import Any

import pypdf
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_mortgage_eeuu.config import Settings, get_settings
from rag_mortgage_eeuu.embeddings import embed_documents
from rag_mortgage_eeuu.vector_store import clear_index, upsert

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _normalize(text: str) -> str:
    return " ".join(text.split())


def chunk_text(text: str, settings: Settings | None = None) -> list[str]:
    settings = settings or get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
    )
    pieces = splitter.split_text(_normalize(text))
    return [p.strip() for p in pieces if len(p.strip()) >= settings.min_chunk_chars]


def load_chunks(settings: Settings | None = None) -> list[dict[str, Any]]:
    settings = settings or get_settings()
    pdf_dir = _PROJECT_ROOT / settings.pdf_dir
    chunks: list[dict[str, Any]] = []
    for path in sorted(pdf_dir.glob("*.pdf")):
        reader = pypdf.PdfReader(str(path))
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            for index, piece in enumerate(chunk_text(text, settings)):
                chunks.append(
                    {
                        "id": f"{path.stem}-p{page_number}-c{index}",
                        "source": path.name,
                        "page": page_number,
                        "text": piece,
                    }
                )
    return chunks


def _embed_in_batches(
    texts: list[str], settings: Settings | None = None
) -> list[list[float]]:
    settings = settings or get_settings()
    size = settings.embed_batch_size
    vectors: list[list[float]] = []
    for start in range(0, len(texts), size):
        vectors.extend(embed_documents(texts[start : start + size], settings))
        if start + size < len(texts):
            time.sleep(settings.embed_batch_pause_seconds)
    return vectors


def ingest(clear: bool = True, settings: Settings | None = None) -> int:
    settings = settings or get_settings()
    chunks = load_chunks(settings)
    if not chunks:
        return 0
    if clear:
        clear_index(settings)
    embeddings = _embed_in_batches([c["text"] for c in chunks], settings)
    vectors: list[dict[str, Any]] = [
        {
            "id": chunk["id"],
            "values": embedding,
            "metadata": {
                "source": chunk["source"],
                "page": chunk["page"],
                "text": chunk["text"],
            },
        }
        for chunk, embedding in zip(chunks, embeddings, strict=True)
    ]
    for start in range(0, len(vectors), 100):
        upsert(vectors[start : start + 100], settings)
    return len(chunks)


def main() -> None:
    load_dotenv()
    count = ingest()
    print(f"Ingested {count} chunks from PDFs into the knowledge base.")


if __name__ == "__main__":
    main()

import contextlib
import time
from typing import Any

from pinecone import Pinecone, ServerlessSpec

from rag_mortgage_eeuu.config import Settings, get_settings


def _require_pinecone_key(settings: Settings) -> str:
    if not settings.pinecone_api_key:
        raise RuntimeError(
            "PINECONE_API_KEY is not set. Add it to .env to use retrieval."
        )
    return settings.pinecone_api_key


def _client(settings: Settings | None = None) -> Pinecone:
    s = settings or get_settings()
    api_key = _require_pinecone_key(s)
    return Pinecone(api_key=api_key)


def ensure_index(settings: Settings | None = None) -> Any:
    settings = settings or get_settings()
    pc = _client(settings)
    existing = {index["name"] for index in pc.list_indexes()}
    if settings.pinecone_index not in existing:
        pc.create_index(
            name=settings.pinecone_index,
            dimension=settings.embed_dim,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=settings.pinecone_cloud, region=settings.pinecone_region
            ),
        )
        for _ in range(30):
            if pc.describe_index(settings.pinecone_index)["status"]["ready"]:
                break
            time.sleep(1)
    return pc.Index(settings.pinecone_index)


def upsert(vectors: list[dict[str, Any]], settings: Settings | None = None) -> None:
    ensure_index(settings).upsert(vectors=vectors)


def clear_index(settings: Settings | None = None) -> None:
    with contextlib.suppress(Exception):
        ensure_index(settings).delete(delete_all=True)


def query(
    vector: list[float],
    top_k: int,
    settings: Settings | None = None,
) -> list[dict[str, Any]]:
    response = ensure_index(settings).query(
        vector=vector, top_k=top_k, include_metadata=True
    )
    return [
        {"score": match["score"], "metadata": match["metadata"]}
        for match in response["matches"]
    ]

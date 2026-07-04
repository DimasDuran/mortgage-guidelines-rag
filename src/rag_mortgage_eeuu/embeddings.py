import time

import httpx

from rag_mortgage_eeuu.config import Settings, get_settings

_BASE_URL = "https://api.voyageai.com/v1"
_TIMEOUT = 60.0
_MAX_RETRIES = 5


def _headers(settings: Settings) -> dict[str, str]:
    if not settings.voyage_api_key:
        raise RuntimeError(
            "VOYAGE_API_KEY is not set. Add it to .env to use retrieval."
        )
    return {
        "Authorization": f"Bearer {settings.voyage_api_key}",
        "Content-Type": "application/json",
    }


def _post_with_retry(url: str, headers: dict, json: dict) -> httpx.Response:
    for attempt in range(_MAX_RETRIES):
        response = httpx.post(url, headers=headers, json=json, timeout=_TIMEOUT)
        if response.status_code == 429:
            wait = min(2 ** attempt * 4, 120)
            print(f"  rate limited, retrying in {wait}s (attempt {attempt + 1}/{_MAX_RETRIES})")
            time.sleep(wait)
            continue
        response.raise_for_status()
        return response
    raise RuntimeError(f"Failed after {_MAX_RETRIES} retries due to rate limiting.")


def _embed(
    texts: list[str], input_type: str, settings: Settings | None = None
) -> list[list[float]]:
    settings = settings or get_settings()
    response = _post_with_retry(
        f"{_BASE_URL}/embeddings",
        headers=_headers(settings),
        json={"input": texts, "model": settings.embed_model, "input_type": input_type},
    )
    data = response.json()["data"]
    return [item["embedding"] for item in data]


def embed_documents(
    texts: list[str], settings: Settings | None = None
) -> list[list[float]]:
    return _embed(texts, "document", settings)


def embed_query(
    text: str, settings: Settings | None = None
) -> list[float]:
    return _embed([text], "query", settings)[0]


def rerank(
    query: str,
    documents: list[str],
    top_k: int,
    settings: Settings | None = None,
) -> list[tuple[int, float]]:
    settings = settings or get_settings()
    response = _post_with_retry(
        f"{_BASE_URL}/rerank",
        headers=_headers(settings),
        json={
            "query": query,
            "documents": documents,
            "model": settings.rerank_model,
            "top_k": top_k,
        },
    )
    data = response.json()["data"]
    return [(item["index"], item["relevance_score"]) for item in data]

from rag_mortgage_eeuu import vector_store
from rag_mortgage_eeuu.config import Settings, get_settings
from rag_mortgage_eeuu.embeddings import embed_query, rerank


def search(
    question: str, k: int | None = None, settings: Settings | None = None
) -> list[dict[str, object]]:
    settings = settings or get_settings()
    k = k or settings.retrieval_k

    query_vector = embed_query(question, settings)
    candidates = vector_store.query(
        query_vector, top_k=settings.retrieval_candidates, settings=settings
    )
    if not candidates:
        return []

    documents = [str(c["metadata"]["text"]) for c in candidates]
    top = min(k, len(documents))
    ranked = rerank(question, documents, top_k=top, settings=settings)

    results: list[dict[str, object]] = []
    for index, score in ranked:
        metadata = candidates[index]["metadata"]
        results.append(
            {
                "source": metadata["source"],
                "page": metadata["page"],
                "text": metadata["text"],
                "score": score,
            }
        )
    return results

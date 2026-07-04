# RAG Mortgage EEUU

Sistema RAG (Retrieval-Augmented Generation) para la base de conocimiento hipotecaria de EE.UU.

## Stack

- **Embeddings + Reranking:** Voyage AI (`voyage-3`, `rerank-2`)
- **Vector store:** Pinecone (serverless, AWS us-east-1, cosine similarity)
- **Chunking:** `RecursiveCharacterTextSplitter` (LangChain)
- **PDF parsing:** `pypdf`

## Requisitos

- Python 3.11+
- Poetry

## Instalación

```bash
poetry install
```

## Configuración

Copia `.env.example` a `.env` y completa las API keys:

```
VOYAGE_API_KEY=...
PINECONE_API_KEY=...
```

## Uso

### Ingestar PDFs en la base de conocimiento

```bash
poetry run python -m rag_mortgage_eeuu.ingest
```

### Buscar en la base de conocimiento (prueba rápida)

```bash
poetry run python -c "
from rag_mortgage_eeuu.retriever import search
for r in search('What is LTV?'):
    print(f\"  [{r['source']}:p{r['page']}] (score={r['score']:.3f})\\n    {r['text'][:200]}...\\n\")
"
```

## Tests

```bash
poetry run pytest
```

## Arquitectura

```
rag_mortgage_eeuu/
├── src/rag_mortgage_eeuu/
│   ├── config.py        # Settings (pydantic-settings)
│   ├── embeddings.py    # Voyage AI: embeddings + reranking via httpx
│   ├── vector_store.py  # Pinecone: index, upsert, query, clear
│   ├── retriever.py     # Orquestación: embed → Pinecone → rerank
│   └── ingest.py        # Pipeline: PDF → chunk → embed → upsert
├── pdf/                 # Source PDFs
└── tests/
```

Flujo de retrieval:
1. `embed_query(question)` → Voyage
2. `Pinecone.query(vector, top_k=10)` → 10 candidatos
3. `rerank(question, docs, top_k=4)` → Voyage, top 4 precisos
4. Resultados: `[{source, page, text, score}]`

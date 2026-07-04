# Mortgage Guidelines RAG

A retrieval-augmented generation (RAG) pipeline over official United States
mortgage guidelines. It ingests PDF documents from regulatory bodies and
government-sponsored enterprises — including the CFPB, FHA, VA, Fannie Mae,
Freddie Mac, and the Uniform Residential Loan Application (URLA / Form 1003) —
into a vector search index and serves citation-grounded answers.

## Problem

Mortgage origination in the United States is governed by a dense web of
regulations, program guidelines, and disclosure requirements. Lenders such as
Bank of America provide program overviews on their public site
([https://www.bankofamerica.com/mortgage/home-mortgage/](https://www.bankofamerica.com/mortgage/home-mortgage/)),
but loan officers, processors, and compliance staff must consult dozens of
official documents — the CFPB shopping toolkit, FHA handbooks, VA lender
guides, and URLA instructions — to answer specific questions accurately.

A knowledge gap on any of these documents can slow down processing, lead to
compliance risk, or result in incomplete borrower guidance. This pipeline
centralises the reference corpus, chunks it for precise retrieval, and lets
LLM applications query it with citations back to the original source
(paragraph, page, document name).

## Stack

- **Embeddings + Reranking:** Voyage AI (`voyage-3`, `rerank-2`)
- **Vector store:** Pinecone (serverless, AWS us-east-1, cosine similarity)
- **Chunking:** `RecursiveCharacterTextSplitter` (LangChain)
- **PDF parsing:** `pypdf`
- **Evaluation:** LangSmith, Ragas
- **Interface:** Gradio (optional)
- **Packaging:** Poetry

## Retrieval flow

```
question → embed_query (Voyage) → Pinecone query (top-10)
  → rerank (Voyage, top-4) → [{source, page, text, score}]
```

## Setup

```bash
poetry install
cp .env.example .env   # set VOYAGE_API_KEY, PINECONE_API_KEY
```

## Usage

### Ingest PDFs

```bash
poetry run python -m rag_mortgage_eeuu.ingest
```

### Search (quick test)

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

## Architecture

```
src/rag_mortgage_eeuu/
  config.py        # settings (pydantic-settings)
  embeddings.py    # Voyage AI: embeddings + reranking via httpx
  vector_store.py  # Pinecone: index, upsert, query, clear
  retriever.py     # orchestration: embed → Pinecone → rerank
  ingest.py        # pipeline: PDF → chunk → embed → upsert
  main.py          # Gradio interface
pdf/               # source PDF documents
evals/             # evaluation scripts (LangSmith, Ragas)
tests/
```

## License

MIT

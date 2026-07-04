import pytest

from rag_mortgage_eeuu.config import get_settings
from rag_mortgage_eeuu.ingest import _normalize, chunk_text


def test_normalize_collapses_whitespace():
    assert _normalize("a   b\n\n c\t d") == "a b c d"


def test_chunk_text_splits_long_text_and_filters_tiny(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("VOYAGE_API_KEY", "sk-test")
    monkeypatch.setenv("PINECONE_API_KEY", "sk-test")
    get_settings.cache_clear()

    chunks = chunk_text("Mortgage guidance. " * 400)
    assert len(chunks) > 1
    threshold = get_settings().min_chunk_chars
    assert all(len(c) >= threshold for c in chunks)


def test_chunk_text_drops_near_empty(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("VOYAGE_API_KEY", "sk-test")
    monkeypatch.setenv("PINECONE_API_KEY", "sk-test")
    get_settings.cache_clear()
    assert chunk_text("   ") == []

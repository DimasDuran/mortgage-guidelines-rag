from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    voyage_api_key: str | None = Field(default=None, validation_alias="VOYAGE_API_KEY")
    pinecone_api_key: str | None = Field(
        default=None, validation_alias="PINECONE_API_KEY"
    )
    embed_model: str = "voyage-3"
    embed_dim: int = 1024
    rerank_model: str = "rerank-2"
    pinecone_index: str = "vera-knowledge"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    retrieval_candidates: int = 10
    retrieval_k: int = 4

    pdf_dir: str = "pdf"
    chunk_size: int = 1000
    chunk_overlap: int = 150
    min_chunk_chars: int = 80
    embed_batch_size: int = 30
    embed_batch_pause_seconds: float = 60.0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        protected_namespaces=(),
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

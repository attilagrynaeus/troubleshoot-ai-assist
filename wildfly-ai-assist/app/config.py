"""Centralised runtime configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """All tunables live here so the rest of the code stays clean."""

    # === external services ===
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    confluence_base_url: str = Field(..., env="CONFLUENCE_URL")
    confluence_token: str = Field(..., env="CONFLUENCE_TOKEN")
    confluence_space: str = Field(..., env="CONFLUENCE_SPACE")

    # === local storage ===
    index_path: str = Field("data/faiss_index", description="Where the FAISS files live")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Singleton accessor so importing code never instantiates Settings twice."""
    return Settings()

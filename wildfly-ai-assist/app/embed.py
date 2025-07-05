"""Chunk → embed → FAISS.

    poetry run python -m app.embed
"""

from pathlib import Path

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding

from .config import get_settings

settings = get_settings()
PAGES_DIR = Path("data/pages")
INDEX_DIR = Path(settings.index_path)
CHUNK_SIZE = 800
CHUNK_OVERLAP = 80


def build_index() -> None:
    """Create or rebuild a FAISS vector index from local markdown files."""
    docs = SimpleDirectoryReader(str(PAGES_DIR)).load_data()
    embedder = OpenAIEmbedding(
        model_name="text-embedding-3-small", api_key=settings.openai_api_key
    )
    index = VectorStoreIndex.from_documents(
        docs,
        embed_model=embedder,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    index.storage_context.persist(persist_dir=str(INDEX_DIR))
    print(f"✓ index saved to '{INDEX_DIR}'")


if __name__ == "__main__":  # pragma: no cover
    build_index()

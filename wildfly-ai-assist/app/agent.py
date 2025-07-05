"""Thin wrapper around a LlamaIndex RetrieverQueryEngine."""

from pathlib import Path
from typing import List

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI

from .config import get_settings

settings = get_settings()
INDEX_DIR = Path(settings.index_path)

# -- lazy singletons ---------------------------------------------------------

def _create_engine() -> RetrieverQueryEngine:
    """Initialise the FAISS-backed query engine."""
    storage = StorageContext.from_defaults(persist_dir=str(INDEX_DIR))
    index = load_index_from_storage(storage)

    retriever = index.as_retriever(similarity_top_k=4)
    llm = OpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key)  # cheaper variant

    return RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=llm,
        response_mode="compact",
    )


_engine: RetrieverQueryEngine | None = None


def _get_engine() -> RetrieverQueryEngine:
    global _engine
    if _engine is None:
        _engine = _create_engine()
    return _engine


# -- public API --------------------------------------------------------------


def ask(question: str) -> str:
    """Return a concise answer for the given stack trace or question."""
    if not question.strip():
        return "Input is empty."
    return str(_get_engine().query(question))

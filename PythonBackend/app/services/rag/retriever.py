"""
Retrieval module used by the LIVE API at request time.

Imports the persistent Chroma collection and runs semantic similarity queries
using the lightweight ONNX DefaultEmbeddingFunction.
"""

from pathlib import Path
import chromadb
import chromadb.utils.embedding_functions as ef
import logging

logger = logging.getLogger(__name__)

APP_DIR = Path(__file__).resolve().parent.parent.parent
CHROMA_STORE_PATH = APP_DIR.parent / "chroma_store"
COLLECTION_NAME = "ayurveda_knowledge"

_embedding_fn = ef.DefaultEmbeddingFunction()
_client = chromadb.PersistentClient(path=str(CHROMA_STORE_PATH))
_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=_embedding_fn
)


def retrieve_relevant_context(query: str, top_k: int = 3) -> list[str]:
    """Given a natural-language query, return the top_k most semantically
    similar chunks stored in the knowledge base.
    """
    try:
        count = _collection.count()
        if count == 0:
            logger.warning("Knowledge base is empty. Attempting auto-rebuild.")
            from .ingest import build_knowledge_base
            build_knowledge_base(force=False)
            count = _collection.count()

        if count == 0:
            return []

        results = _collection.query(
            query_texts=[query],
            n_results=min(top_k, count),
        )
        if results and "documents" in results and results["documents"]:
            return results["documents"][0]
        return []
    except Exception as e:
        logger.error(f"Error retrieving context from Chroma: {e}")
        return []

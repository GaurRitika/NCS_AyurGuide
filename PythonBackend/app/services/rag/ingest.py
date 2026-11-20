"""
One-time ingestion module for the RAG knowledge base.

WHAT THIS DOES:
  1. Reads all raw source text files from app/data/knowledge_base/ (.txt)
  2. Splits text into coherent paragraph-level chunks
  3. Uses ChromaDB's built-in lightweight ONNX embedding engine (fast, <80MB, zero PyTorch dependency)
  4. Stores chunk text + embeddings into a persistent Chroma collection on disk

WHY CHROMA'S BUILT-IN ONNX EMBEDDING:
  Traditional sentence-transformers requires PyTorch (~800MB+ download and ~500MB+ RAM),
  which crashes or times out on free cloud tiers (like Render's 512MB limit).
  Chroma's native DefaultEmbeddingFunction runs on an ultra-lightweight ONNX runtime
  using all-MiniLM-L6-v2, consuming under 80MB RAM and running in milliseconds.
"""

from pathlib import Path
import chromadb
import chromadb.utils.embedding_functions as ef
import logging

logger = logging.getLogger(__name__)

# Resolve paths relative to this file
RAG_DIR = Path(__file__).resolve().parent
APP_DIR = RAG_DIR.parent.parent
KNOWLEDGE_BASE_DIR = APP_DIR / "data" / "knowledge_base"
CHROMA_STORE_PATH = APP_DIR.parent / "chroma_store"

COLLECTION_NAME = "ayurveda_knowledge"
_embedding_fn = ef.DefaultEmbeddingFunction()


def load_source_chunks() -> tuple[list[str], list[dict], list[str]]:
    """Read every .txt file in the knowledge base folder and split into
    paragraph-level chunks with metadata."""
    chunks: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []

    txt_files = sorted(KNOWLEDGE_BASE_DIR.glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(
            f"No .txt files found in {KNOWLEDGE_BASE_DIR}. "
            "Add at least one source file before running ingestion."
        )

    chunk_counter = 0
    for txt_file in txt_files:
        text = txt_file.read_text(encoding="utf-8")
        # Split on double newline (paragraphs)
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
        for p in paragraphs:
            chunks.append(p)
            metadatas.append({"source": txt_file.name})
            ids.append(f"doc_{chunk_counter}")
            chunk_counter += 1
        print(f"  Loaded {txt_file.name}: {len(paragraphs)} chunk(s)")

    return chunks, metadatas, ids


def is_knowledge_base_populated() -> bool:
    """Check whether the Chroma collection already has data without re-embedding."""
    try:
        client = chromadb.PersistentClient(path=str(CHROMA_STORE_PATH))
        collection = client.get_collection(name=COLLECTION_NAME, embedding_function=_embedding_fn)
        return collection.count() > 0
    except Exception:
        return False


def build_knowledge_base(force: bool = False) -> int:
    """Build (or rebuild) the vector store from the source .txt files.

    Used both by the manual CLI script (`python -m app.services.rag.ingest`)
    and automatically on startup by FastAPI lifespan.
    """
    if not force and is_knowledge_base_populated():
        print("Knowledge base already populated, skipping rebuild.")
        return 0

    print(f"Reading source files from: {KNOWLEDGE_BASE_DIR}")
    chunks, metadatas, ids = load_source_chunks()
    print(f"Total chunks to embed: {len(chunks)}")

    print(f"Writing to persistent Chroma store at: {CHROMA_STORE_PATH}")
    client = chromadb.PersistentClient(path=str(CHROMA_STORE_PATH))

    # Clean previous collection if it exists
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=_embedding_fn
    )

    # Ingest in small batches to keep memory usage minimal
    batch_size = 20
    for i in range(0, len(chunks), batch_size):
        end = min(i + batch_size, len(chunks))
        collection.add(
            documents=chunks[i:end],
            metadatas=metadatas[i:end],
            ids=ids[i:end]
        )

    print(f"Ingestion complete. {len(chunks)} chunks stored in collection '{COLLECTION_NAME}'.")
    return len(chunks)


if __name__ == "__main__":
    # Manual execution forces rebuild
    build_knowledge_base(force=True)

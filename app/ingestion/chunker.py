"""Split documents into overlapping word windows."""
from app.core.models import Chunk, Document

def chunk_document(doc: Document, chunk_size: int = 200, overlap: int = 50) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")


    # Title carries strong signal in scientific text, so include it in the first chunk
    full_text = f"{doc.title}. {doc.text}" if doc.title else doc.text
    words = full_text.split()
    if not words:
        return []

    step = chunk_size - overlap
    chunks: list[Chunk] = []
    for position, start in enumerate(range(0, len(words), step)):
        window = words[start : start + chunk_size]
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}#{position}",
                doc_id=doc.doc_id,
                text=" ".join(window),
                position=position,
            )
        )
        if start + chunk_size >= len(words):   # this window reached the end
            break
    return chunks

def chunk_corpus(corpus: dict[str, Document], chunk_size: int = 200, overlap: int = 50) -> list[Chunk]:
    return [c for doc in corpus.values() for c in chunk_document(doc, chunk_size, overlap)]
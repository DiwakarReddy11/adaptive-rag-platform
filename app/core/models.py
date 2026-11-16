"""Core data types used across the whole system."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    text: str

@dataclass(frozen=True)
class Chunk:
    chunk_id: str      # e.g. "4983#0"  -> doc 4983, first chunk
    doc_id: str        # link back to the parent document (needed for BEIR scoring)
    text: str
    position: int      # index of this chunk inside its document

@dataclass(frozen=True)
class Query:
    query_id: str
    text: str
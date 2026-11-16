import pytest

from app.core.models import Document
from app.ingestion.chunker import chunk_document


def make_doc(n_words: int, title: str = "") -> Document:
    return Document(doc_id="d1", title=title, text=" ".join(f"w{i}" for i in range(n_words)))

def test_short_doc_gives_one_chunk_with_title():
    chunks = chunk_document(make_doc(10, title="My Title"))
    assert len(chunks) == 1
    assert chunks[0].text.startswith("My Title.")
    assert chunks[0].chunk_id == "d1#0"


def test_long_doc_has_overlap():
    chunks = chunk_document(make_doc(450), chunk_size=200, overlap=50)
    assert len(chunks) == 3
    first, second = chunks[0].text.split(), chunks[1].text.split()
    assert first[-50:] == second[:50]          # last 50 words repeated


def test_all_chunks_keep_parent_doc_id():
    chunks = chunk_document(make_doc(1000))
    assert all(c.doc_id == "d1" for c in chunks)


def test_empty_doc_returns_no_chunks():
    assert chunk_document(Document(doc_id="e", title="", text="   ")) == []


def test_invalid_overlap_raises():
    with pytest.raises(ValueError):
        chunk_document(make_doc(10), chunk_size=100, overlap=100)
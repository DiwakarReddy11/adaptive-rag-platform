"""Print dataset statistics. Usage: python -m scripts.inspect_data"""
from pathlib import Path
from statistics import mean

from app.ingestion.chunker import chunk_corpus
from app.ingestion.loader import load_corpus, load_qrels, load_queries


DATA = Path("data/scifact")

corpus = load_corpus(DATA)
queries = load_queries(DATA)
qrels = load_qrels(DATA, "test")
chunks = chunk_corpus(corpus)

doc_lengths = [len(f"{d.title} {d.text}".split()) for d in corpus.values()]

print(f"Documents         : {len(corpus)}")
print(f"All queries       : {len(queries)}")
print(f"Test queries      : {len(qrels)}")
print(f"Avg doc length    : {mean(doc_lengths):.0f} words (max {max(doc_lengths)})")
print(f"Chunks            : {len(chunks)}")

qid = next(iter(qrels))
print(f"\nExample query  [{qid}]: {queries[qid].text}")
for doc_id in qrels[qid]:
    print(f"Relevant doc [{doc_id}]: {corpus[doc_id].title}")
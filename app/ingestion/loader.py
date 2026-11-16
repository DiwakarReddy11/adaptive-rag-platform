"""Read BEIR-format files into our domain models."""
import csv
import json
from collections import defaultdict
from pathlib import Path

from app.core.models import Document, Query

def load_corpus(data_dir: Path) -> dict[str, Document]:
    corpus: dict[str, Document] = {}
    with open(data_dir / "corpus.jsonl", encoding="utf-8") as f:
        for line in f:                       # JSONL = one JSON object per line
            row = json.loads(line)
            corpus[row["_id"]] = Document(
                doc_id=row["_id"],
                title=row.get("title", ""),
                text=row.get("text", ""),
            )
    return corpus

def load_queries(data_dir: Path) -> dict[str, Query]:
    queries: dict[str, Query] = {}
    with open(data_dir / "queries.jsonl", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            queries[row["_id"]] = Query(query_id=row["_id"], text=row["text"])
    return queries

def load_qrels(data_dir: Path, split: str = "test") -> dict[str, dict[str, int]]:
    """Returns {query_id: {doc_id: relevance_score}}."""
    qrels: dict[str, dict[str, int]] = defaultdict(dict)
    with open(data_dir / "qrels" / f"{split}.tsv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)                          # skip header row
        for query_id, doc_id, score in reader:
            qrels[query_id][doc_id] = int(score)
    return dict(qrels)
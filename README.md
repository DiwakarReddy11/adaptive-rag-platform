# Adaptive Multi-Strategy RAG Retrieval Platform

A FastAPI service that routes each query to the best retrieval strategy
(BM25, dense, hybrid, HyDE), generates grounded answers with an LLM,
and is benchmarked with BEIR (retrieval) and RAGAS (generation).

## Quickstart
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
pytest
```

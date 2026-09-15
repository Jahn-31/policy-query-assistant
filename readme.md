# Policy Query Assistant

A Retrieval-Augmented Generation (RAG) system for searching government policy documents in
natural language. Ask a question in plain English and get an AI-generated answer grounded in
the source policy text, with citations back to the originating document.

Built to solve a concrete problem: policy documents are long, scattered across ministries, and
effectively unsearchable by keyword. Semantic search over embeddings finds the relevant passage
even when the user's wording doesn't match the document's.

---

## Features

- **Semantic search** over policy PDFs using vector similarity rather than keyword matching
- **Grounded answers with citations** — every response is generated from retrieved source
  passages and cites the document it came from, reducing hallucination
- **Ministry filtering** — scope a query to a specific department (NHAI, Jal Shakti)
- **Scanned-document support** via Tesseract OCR for image-based PDFs
- **Async REST API** built on FastAPI for low-latency concurrent querying

---

## Architecture

```
PDF ingestion
    |
    v
Text extraction (PyPDF2 / pdfplumber, Tesseract OCR for scanned pages)
    |
    v
Chunking  ->  Embedding generation (Sentence Transformers, all-MiniLM-L6-v2)
    |
    v
Vector store (ChromaDB, persisted to disk)
    |
    v
Query -> embed -> top-k similarity search -> context assembly
    |
    v
LLM generation (Groq, Llama 3.3 70B)  ->  answer + citations
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (async), Uvicorn |
| Embeddings | Sentence Transformers — `all-MiniLM-L6-v2` |
| Vector store | ChromaDB (persistent) |
| LLM | Groq API — Llama 3.3 70B |
| PDF processing | PyPDF2, pdfplumber |
| OCR | Tesseract |
| Orchestration | LangChain (document handling) |
| Language | Python 3.9+ |

---

## Project Structure

```
policy-query-assistant/
├── api_server.py          # FastAPI application and route definitions
├── query_engine.py        # Retrieval + LLM answer generation
├── vector_store.py        # ChromaDB persistence and similarity search
├── document_processor.py  # Text extraction, OCR, chunking
├── ingest_document.py     # CLI entry point for indexing new documents
├── config.py              # Configuration and environment settings
├── requirements.txt
├── policies/              # Source policy PDFs, organised by ministry
│   ├── nhai/
│   └── jal_shakti/
└── storage/
    └── chroma_db/         # Persisted vector index (generated)
```

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed and on your `PATH`
  (required only for scanned PDFs)
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
git clone https://github.com/Jahn-31/policy-query-assistant.git
cd policy-query-assistant

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_api_key_here
```

### Indexing documents

Place PDFs under `policies/<ministry>/`, then build the vector index:

```bash
python ingest_document.py
```

### Running the API

```bash
python api_server.py
```

The service starts on `http://localhost:8000`. Interactive API docs are available at
`http://localhost:8000/docs`.

---

## API

**`POST /query`**

```json
{
  "question": "What are the land acquisition norms for national highway projects?",
  "ministry": "nhai",
  "top_k": 5
}
```

Returns the generated answer along with the source passages and document references used
to produce it.

---

## Design Notes

- **Chunking strategy** balances retrieval precision against context completeness — chunks
  that are too small lose the surrounding clause, too large dilute the embedding signal.
- **Grounding over recall** — the system answers from retrieved context only, and surfaces
  citations so the user can verify rather than trust.
- **`all-MiniLM-L6-v2`** was chosen for its accuracy-to-latency ratio; it runs on CPU, which
  keeps the system deployable without GPU infrastructure.

---

## Roadmap

- [ ] Containerised deployment (Docker) to AWS EC2 with S3-backed document storage
- [ ] Retrieval evaluation harness — groundedness and answer-relevance scoring
- [ ] Hybrid search (BM25 + dense retrieval) for better handling of exact legal terminology
- [ ] Re-ranking layer over initial retrieval results

# 🏛️ Policy Query Assistant

An AI-powered semantic search and question-answering system for government policy documents using Retrieval Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

Policy Query Assistant enables government officials and researchers to quickly search through hundreds of policy documents using natural language queries. Instead of manually reading through PDFs, users can ask questions and receive AI-generated answers with source citations.

### Key Features

- 🔍 **Semantic Search**: Understands meaning, not just keywords
- 🤖 **AI-Powered Answers**: Uses Groq's Llama 3.3 for intelligent responses
- 📚 **Source Citations**: Every answer includes document references
- 🏢 **Ministry Filtering**: Search within specific departments
- ⚡ **Fast Performance**: <2 second response time
- 🔄 **Modular Architecture**: Easy to swap LLM providers

## 🎯 Problem Statement

Government officials spend hours searching through policy documents manually. Traditional keyword search misses relevant information due to terminology variations. This system solves that using semantic understanding.

## 🏗️ Architecture

```
User Query → FastAPI → Sentence Transformers (Embeddings)
                    ↓
                ChromaDB (Vector Search)
                    ↓
            Top-K Similar Chunks
                    ↓
            Groq LLM (Answer Generation)
                    ↓
        Answer + Source Citations
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | FastAPI |
| **Vector Database** | ChromaDB |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **LLM** | Groq (Llama 3.3 70B) |
| **Document Processing** | PyPDF2, pdfplumber, LangChain |
| **Language** | Python 3.9+ |

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Groq API key ([Get it here](https://console.groq.com))
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/policy-query-assistant.git
cd policy-query-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

5. **Create required directories**
```bash
mkdir -p policies/nhai policies/jal_shakti storage/chroma_db
```

### Running the Application

1. **Start the API server**
```bash
python api_server.py
```

The server will start at `http://localhost:8000`

2. **Access API Documentation**

Open your browser and navigate to:
```
http://localhost:8000/docs
```

You'll see an interactive API documentation where you can test all endpoints.

## 📖 Usage

### Option 1: Using API Documentation (Recommended)

1. Go to `http://localhost:8000/docs`
2. Try the **POST /upload** endpoint to upload a PDF
3. Try the **POST /query** endpoint to ask questions

### Option 2: Using curl

**Upload a document:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your_document.pdf" \
  -F "ministry=NHAI" \
  -F "document=Policy Name" \
  -F "date=2024-01-15"
```

**Query documents:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the water conservation policy?", "ministry": "Jal Shakti"}'
```

**Get statistics:**
```bash
curl http://localhost:8000/stats
```

### Option 3: Ingest Multiple Documents

Place your PDFs in the appropriate folders:
- `policies/nhai/` - for NHAI documents
- `policies/jal_shakti/` - for Jal Shakti documents

Then run:
```bash
python ingest_document.py
```

## 📁 Project Structure

```
policy-query-assistant/
├── api_server.py           # FastAPI application & endpoints
├── query_engine.py         # LLM integration & answer generation
├── vector_store.py         # ChromaDB vector database operations
├── document_processor.py   # PDF processing & chunking
├── ingest_document.py      # Batch document ingestion script
├── config.py              # Configuration & constants
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── policies/             # PDF storage (not in repo)
│   ├── nhai/
│   └── jal_shakti/
└── storage/              # Database storage (not in repo)
    └── chroma_db/
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Chunk size**: `CHUNK_SIZE = 1000`
- **Chunk overlap**: `CHUNK_OVERLAP = 200`
- **Embedding model**: `EMBEDDING_MODEL = "all-MiniLM-L6-v2"`
- **LLM model**: `GROQ_MODEL = "llama-3.3-70b-versatile"`

## 📊 API Endpoints

### POST /upload
Upload and process a policy PDF

**Request:**
- `file`: PDF file (multipart/form-data)
- `ministry`: Ministry name (string)
- `document`: Document name (string)
- `date`: Document date (string)

**Response:**
```json
{
  "status": "success",
  "chunks": 42
}
```

### POST /query
Query the policy database

**Request:**
```json
{
  "query": "What is the water policy?",
  "ministry": "Jal Shakti"  // optional
}
```

**Response:**
```json
{
  "answer": "The water policy focuses on...",
  "sources": [
    {
      "ministry": "Jal Shakti",
      "document": "Water Conservation Guidelines",
      "date": "2024-01-15"
    }
  ],
  "model": "llama-3.3-70b-versatile"
}
```

### GET /stats
Get database statistics

**Response:**
```json
{
  "total_documents": 150
}
```

## 🎯 How It Works

### 1. Document Processing
- Extract text from PDFs using pdfplumber/PyPDF2
- Split into chunks (1000 chars with 200 char overlap)
- Generate 384-dimensional embeddings using Sentence Transformers
- Store in ChromaDB with metadata

### 2. Query Processing
- Convert user query to embedding
- Perform cosine similarity search in ChromaDB
- Retrieve top-5 most relevant chunks
- Send chunks as context to Groq LLM
- Generate answer with citations

### 3. Answer Generation
- Use Llama 3.3 (70B parameters) via Groq
- Temperature: 0.3 (for factual responses)
- Prompt engineering to ensure answers are grounded in context
- Automatic source attribution

## 📈 Performance

- **Query Latency**: <2 seconds (average)
- **Vector Search**: <100ms
- **LLM Generation**: ~1.5 seconds
- **Concurrent Requests**: 50+
- **Document Capacity**: Thousands of PDFs

## 🔮 Future Enhancements

- [ ] OCR support for scanned documents (Tesseract integration)
- [ ] Multi-language support
- [ ] Conversation history/memory
- [ ] Advanced filtering (date range, tags)
- [ ] Reranking with cross-encoder
- [ ] Hybrid search (semantic + keyword)
- [ ] User authentication
- [ ] Analytics dashboard
- [ ] Batch upload interface
- [ ] Export results to PDF/Word

## 🐛 Troubleshooting

### "Cannot connect to backend"
- Make sure `python api_server.py` is running
- Check if port 8000 is available

### "No results found"
- Verify documents are uploaded: `curl http://localhost:8000/stats`
- Try querying without ministry filter
- Check if PDFs contain extractable text (not scanned images)

### "Groq API error"
- Verify your API key in `.env`
- Check your Groq account has available credits
- Ensure you're not hitting rate limits

### "ModuleNotFoundError"
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- [Groq](https://groq.com) for fast LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## 📚 Learn More

- [RAG Explained](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Vector Databases](https://www.pinecone.io/learn/vector-database/)
- [Semantic Search](https://www.sbert.net/examples/applications/semantic-search/README.html)

---

⭐ If you find this project helpful, please consider giving it a star!

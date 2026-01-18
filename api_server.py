from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import traceback

from document_processor import DocumentProcessor
from vector_store import VectorStore
from query_engine import QueryEngine

app = FastAPI(title="Policy Query Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize with error handling
try:
    processor = DocumentProcessor()
    vector_store = VectorStore()
    query_engine = QueryEngine()
    print("✓ All components initialized successfully")
except Exception as e:
    print(f"✗ Initialization error: {e}")
    traceback.print_exc()

class QueryRequest(BaseModel):
    query: str
    ministry: str = None

@app.get("/")
async def root():
    return {
        "message": "Policy Query Assistant API",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "upload": "POST /upload",
            "query": "POST /query",
            "stats": "GET /stats"
        }
    }

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    ministry: str = Form(...),
    document: str = Form(...),
    date: str = Form(...)
):
    """Upload and process a policy PDF"""
    try:
        # Save file
        path = f"policies/{ministry}/{file.filename}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Process
        metadata = {"ministry": ministry, "document": document, "date": date}
        chunks = processor.process(path, metadata)
        vector_store.add_documents(chunks)
        
        return {"status": "success", "chunks": len(chunks)}
    except Exception as e:
        print(f"Upload error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(request: QueryRequest):
    """Query the policy database"""
    try:
        print(f"\n--- New Query ---")
        print(f"Query: {request.query}")
        print(f"Ministry filter: {request.ministry}")
        
        # Search
        print("Searching vector store...")
        chunks = vector_store.search(
            request.query,
            ministry=request.ministry
        )
        print(f"Found {len(chunks)} chunks")
        
        if not chunks:
            return {
                "answer": "No relevant documents found for your query.",
                "sources": []
            }
        
        # Generate answer
        print("Generating answer...")
        result = query_engine.answer(request.query, chunks)
        print("Answer generated successfully")
        
        return result
        
    except Exception as e:
        print(f"\n✗ Query error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail={
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        })

@app.get("/stats")
async def stats():
    """Get database statistics"""
    try:
        count = vector_store.collection.count()
        return {"total_documents": count, "status": "ok"}
    except Exception as e:
        print(f"Stats error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
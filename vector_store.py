import uuid
import chromadb
from sentence_transformers import SentenceTransformer
import config
import uuid

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.collection = self.client.get_or_create_collection("policies")
    
    def add_documents(self, chunks):
        """Add chunks to vector database"""
        texts = [c['text'] for c in chunks]
        metas = [c['metadata'] for c in chunks]
        if not chunks:
            print("⚠️ No chunks to add, skipping document")
            return
        embeddings = self.embedding_model.encode(texts).tolist()
        ids = [
            f"{m['ministry']}_{m['document']}_{m['chunk_id']}_{uuid.uuid4().hex}"
            for m in metas
        ]
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metas,
            ids=ids
        )
        print(f"Added {len(chunks)} chunks")
    
    def search(self, query, n_results=5, ministry=None):
        """Search for relevant chunks"""
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        where = {"ministry": ministry} if ministry else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        return [
            {
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "score": 1 - results['distances'][0][i]
            }
            for i in range(len(results['documents'][0]))
        ]
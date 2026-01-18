import os
from document_processor import DocumentProcessor
from vector_store import VectorStore

def ingest_all_policies():
    """Process all PDFs in the policies folder"""
    processor = DocumentProcessor()
    vector_store = VectorStore()
    
    policies_dir = "policies"
    
    # Process Jal Shakti documents
    jal_shakti_dir = f"{policies_dir}/jal_shakti"
    if os.path.exists(jal_shakti_dir):
        for file in os.listdir(jal_shakti_dir):
            if file.endswith('.pdf'):
                path = f"{jal_shakti_dir}/{file}"
                print(f"Processing: {file}")
                
                metadata = {
                    "ministry": "Jal Shakti",
                    "document": file.replace('.pdf', ''),
                    "date": "2024"
                }
                
                chunks = processor.process(path, metadata)
                vector_store.add_documents(chunks)
    
    # Process NHAI documents
    nhai_dir = f"{policies_dir}/nhai"
    if os.path.exists(nhai_dir):
        for file in os.listdir(nhai_dir):
            if file.endswith('.pdf'):
                path = f"{nhai_dir}/{file}"
                print(f"Processing: {file}")
                
                metadata = {
                    "ministry": "NHAI",
                    "document": file.replace('.pdf', ''),
                    "date": "2024"
                }
                
                chunks = processor.process(path, metadata)
                vector_store.add_documents(chunks)
    
    print("\nIngestion complete!")

if __name__ == "__main__":
    ingest_all_policies()

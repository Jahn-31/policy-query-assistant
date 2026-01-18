import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Paths
CHROMA_DB_PATH = "./storage/chroma_db"
POLICIES_PATH = "./policies"

# Model Settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CLAUDE_MODEL = "claude-sonnet-4-20250514"
GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and accurate

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
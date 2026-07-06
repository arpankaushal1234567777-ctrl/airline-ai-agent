import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# Knowledge Base
# ==========================

KNOWLEDGE_BASE_PATH = "data/knowledge_base"

# ==========================
# Chunking
# ==========================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ==========================
# Embeddings
# ==========================

EMBEDDING_PROVIDER = "huggingface"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ==========================
# ChromaDB
# ==========================

CHROMA_COLLECTION_NAME = "airline_knowledge"
CHROMA_PERSIST_DIRECTORY = "chroma_db"

# ==========================
# Retrieval
# ==========================

RETRIEVAL_K = 4

# ==========================
# LLM Configuration
# ==========================

LLM_PROVIDER = "groq"
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================
# Retrieval
# ==========================

RETRIEVAL_K = 4


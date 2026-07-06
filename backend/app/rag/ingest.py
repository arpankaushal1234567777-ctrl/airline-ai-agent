from app.config import KNOWLEDGE_BASE_PATH

from app.rag.loader import DocumentLoader
from app.rag.cleaner import DocumentCleaner
from app.rag.chunker import DocumentChunker
from app.rag.vector_store import ChromaVectorStore


def ingest():

    loader = DocumentLoader(KNOWLEDGE_BASE_PATH)

    cleaner = DocumentCleaner()

    chunker = DocumentChunker()

    vector_store = ChromaVectorStore()

    documents = loader.load_documents()

    cleaned_documents = cleaner.clean_documents(documents)

    chunks = chunker.chunk_documents(cleaned_documents)

    vector_store.reset_collection()
    
    vector_store.add_documents(chunks)

    print(f"{len(chunks)} chunks stored successfully.")


if __name__ == "__main__":
    ingest()
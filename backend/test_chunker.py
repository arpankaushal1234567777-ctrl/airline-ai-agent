from app.rag.loader import DocumentLoader
from app.rag.cleaner import DocumentCleaner
from app.rag.chunker import DocumentChunker

loader = DocumentLoader("data/knowledge_base")
documents = loader.load_documents()

cleaner = DocumentCleaner()
documents = cleaner.clean_documents(documents)

chunker = DocumentChunker()
chunks = chunker.chunk_documents(documents)

print(f"\nTotal Chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks[:5], start=1):
    print("=" * 60)
    print(f"Chunk {i}")
    print(chunk.metadata)
    print(chunk.page_content[:300])
    print()
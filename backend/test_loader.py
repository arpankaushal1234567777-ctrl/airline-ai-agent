from app.rag.loader import DocumentLoader

loader = DocumentLoader("data/knowledge_base")

documents = loader.load_documents()

print(f"\nLoaded {len(documents)} documents\n")

for doc in documents:
    print("=" * 50)
    print(doc.metadata)
    print(doc.page_content[:200])
    print()
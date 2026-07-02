from app.rag.loader import DocumentLoader
from app.rag.cleaner import DocumentCleaner

loader = DocumentLoader("data/knowledge_base")
documents = loader.load_documents()

cleaner = DocumentCleaner()
cleaned_documents = cleaner.clean_documents(documents)

print(f"Loaded: {len(cleaned_documents)} documents\n")

for document in cleaned_documents:
    print("=" * 50)
    print(document.metadata)
    print(document.page_content[:300])
    print()
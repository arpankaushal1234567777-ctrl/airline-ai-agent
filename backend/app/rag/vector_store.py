from langchain_chroma import Chroma

from app.config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIRECTORY,
)

from app.rag.embeddings.embedding_factory import (
    get_embedding_model,
)


class ChromaVectorStore:

    def __init__(self):

        self.embedding_model = get_embedding_model()

        self.vector_store = Chroma(
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embedding_model,
        )

    def add_documents(self, chunks):

        self.vector_store.add_documents(chunks)

    def as_retriever(self, search_kwargs=None):

        if search_kwargs is None:
            search_kwargs = {"k": 4}

        return self.vector_store.as_retriever(
            search_kwargs=search_kwargs
        )

    def reset_collection(self):
        self.vector_store.delete_collection()

        self.vector_store = Chroma(
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embedding_model,
        )
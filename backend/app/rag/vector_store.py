from langchain_chroma import Chroma

from app.config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIRECTORY,
)

from app.rag.embeddings.embedding_factory import (
    get_embedding_model,
)


def get_vector_store():
    embedding_model = get_embedding_model()

    return Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIRECTORY,
        embedding_function=embedding_model,
    )


def add_documents(chunks):
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)


def delete_collection():
    vector_store = get_vector_store()
    vector_store.delete_collection()
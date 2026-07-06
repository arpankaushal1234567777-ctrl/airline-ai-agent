from typing import List

from langchain_core.documents import Document

from app.config import RETRIEVAL_K
from app.rag.vector_store import ChromaVectorStore


class ChromaRetriever:

    def __init__(self):

        self.vector_store = ChromaVectorStore()

        self.chroma_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": RETRIEVAL_K}
        )

    def retrieve_documents(self, query: str) -> List[Document]:

        return self.chroma_retriever.invoke(query)
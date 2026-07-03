from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Splits cleaned documents into smaller chunks
    for embedding and retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n## ",
                "\n### ",
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks.

        Args:
            documents: Cleaned LangChain Document objects.

        Returns:
            List[Document]: Chunked documents.
        """

        chunks = self.text_splitter.split_documents(documents)

        return chunks
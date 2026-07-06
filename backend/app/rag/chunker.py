from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP


class DocumentChunker:
    """
    Splits cleaned documents into smaller chunks.
    """

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
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

        return self.text_splitter.split_documents(documents)
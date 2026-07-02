from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader


class DocumentLoader:
    """
    Loads all supported knowledge base documents
    from the knowledge_base directory.
    """

    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)

    def load_documents(self) -> List[Document]:
        """
        Load all Markdown documents from the knowledge base.

        Returns:
            List[Document]: List of LangChain Document objects.
        """
        documents = []

        markdown_files = self.knowledge_base_path.glob("*.md")

        for file_path in markdown_files:
            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

            docs = loader.load()

            documents.extend(docs)

        return documents
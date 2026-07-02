import re
from typing import List

from langchain_core.documents import Document


class DocumentCleaner:
    """
    Cleans the text content of LangChain Document objects.
    """

    def clean_documents(self, documents: List[Document]) -> List[Document]:
        """
        Clean all loaded documents.

        Args:
            documents: List of LangChain Document objects.

        Returns:
            List[Document]: Cleaned documents.
        """

        cleaned_documents = []

        for document in documents:
            cleaned_text = self.clean_text(document.page_content)

            cleaned_document = Document(
                page_content=cleaned_text,
                metadata=document.metadata
            )

            cleaned_documents.append(cleaned_document)

        return cleaned_documents

    def clean_text(self, text: str) -> str:
        """
        Clean a single text document.
        """

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove extra spaces and tabs
        text = re.sub(r"[ \t]+", " ", text)

        # Remove multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove leading and trailing whitespace
        text = text.strip()

        return text
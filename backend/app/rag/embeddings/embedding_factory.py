from langchain_huggingface import HuggingFaceEmbeddings

from app.config import (
    EMBEDDING_PROVIDER,
    EMBEDDING_MODEL,
)


def get_embedding_model():
    """
    Returns the configured embedding model.
    """

    if EMBEDDING_PROVIDER == "huggingface":
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

    raise NotImplementedError(
        f"Embedding provider '{EMBEDDING_PROVIDER}' is not supported."
    )
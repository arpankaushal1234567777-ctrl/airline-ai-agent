from langchain_huggingface import HuggingFaceEmbeddings

from app.config import (
    EMBEDDING_PROVIDER,
    EMBEDDING_MODEL,
)


def get_embedding_model():

    if EMBEDDING_PROVIDER == "huggingface":

        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

    raise NotImplementedError(
        f"{EMBEDDING_PROVIDER} is not supported."
    )
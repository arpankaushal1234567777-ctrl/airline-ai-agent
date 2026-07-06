from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import (
    LLM_PROVIDER,
    LLM_MODEL,
    LLM_TEMPERATURE,
)


def get_llm():

    if LLM_PROVIDER.lower() == "groq":
        return ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
        )

    elif LLM_PROVIDER.lower() == "gemini":
        return ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
        )

    else:
        raise ValueError(f"Unsupported LLM Provider: {LLM_PROVIDER}")
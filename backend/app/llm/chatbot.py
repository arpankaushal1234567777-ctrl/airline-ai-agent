from app.llm.llm_factory import get_llm
from app.llm.prompts import RAG_PROMPT
from app.rag.retriever import ChromaRetriever


class AirlineChatbot:

    def __init__(self):

        self.retriever = ChromaRetriever()
        self.llm = get_llm()

    def ask(self, question: str) -> str:

        documents = self.retriever.retrieve_documents(question)

        context = "\n\n".join(
            document.page_content for document in documents
        )

        prompt = RAG_PROMPT.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        response = self.llm.invoke(prompt)

        return response.content
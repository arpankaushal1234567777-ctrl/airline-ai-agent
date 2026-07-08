from langchain_core.messages import HumanMessage, ToolMessage

from app.llm.llm_factory import get_llm
from app.llm.prompts import RAG_PROMPT
from app.llm.tools import ALL_TOOLS, TOOLS_BY_NAME
from app.rag.retriever import ChromaRetriever


class AirlineChatbot:

    def __init__(self):

        self.retriever = ChromaRetriever()
        self.llm = get_llm()

        # LLM with tools bound - used first so the model can decide
        # whether this query needs a function call.
        self.llm_with_tools = self.llm.bind_tools(ALL_TOOLS)

    def ask(self, question: str) -> str:

        messages = [HumanMessage(content=question)]

        response = self.llm_with_tools.invoke(messages)

        # Case 1: model wants to call one or more tools
        if response.tool_calls:

            messages.append(response)

            for tool_call in response.tool_calls:

                tool_fn = TOOLS_BY_NAME.get(tool_call["name"])

                if tool_fn is None:
                    result = {
                        "success": False,
                        "message": f"Unknown tool: {tool_call['name']}",
                    }
                else:
                    result = tool_fn.invoke(tool_call["args"])

                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

            final_response = self.llm_with_tools.invoke(messages)

            return final_response.content

        # Case 2: no tool call needed - fall back to RAG
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

        rag_response = self.llm.invoke(prompt)

        return rag_response.content
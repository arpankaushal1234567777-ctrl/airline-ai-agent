from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from app.llm.llm_factory import get_llm
from app.llm.prompts import TOOL_SYSTEM_PROMPT, TOOL_SUMMARIZATION_PROMPT
from app.llm.tools import ALL_TOOLS, TOOLS_BY_NAME
from app.rag.retriever import ChromaRetriever


class AirlineChatbot:

    def __init__(self):

        self.retriever = ChromaRetriever()
        self.llm = get_llm()

        # LLM with tools bound - used first so the model can decide
        # whether this query needs a function call.
        self.llm_with_tools = self.llm.bind_tools(ALL_TOOLS)

        # Conversation memory - persists across ask() calls.
        # Cleared when reset() is called or the process exits.
        self.messages = [SystemMessage(content=TOOL_SYSTEM_PROMPT)]

    def reset(self):
        """Clear conversation history and start a fresh session."""
        self.messages = [SystemMessage(content=TOOL_SYSTEM_PROMPT)]

    def ask(self, question: str) -> str:

        self.messages.append(HumanMessage(content=question))

        response = self.llm_with_tools.invoke(self.messages)

        # Case 1: model wants to call one or more tools
        if response.tool_calls:

            print(f"[PATH: TOOL] question={question!r} "
                  f"tools_called={[tc['name'] for tc in response.tool_calls]}")

            self.messages.append(response)

            for tool_call in response.tool_calls:

                tool_fn = TOOLS_BY_NAME.get(tool_call["name"])

                if tool_fn is None:
                    result = {
                        "success": False,
                        "message": f"Unknown tool: {tool_call['name']}",
                    }
                else:
                    try:
                        result = tool_fn.invoke(tool_call["args"])
                    except Exception as e:
                        result = {
                            "success": False,
                            "message": f"Tool execution failed: {e}",
                        }

                print(f"[TOOL RESULT] name={tool_call['name']} "
                      f"args={tool_call['args']} result={result}")

                self.messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

            # Summarization prompt is temporary - not kept in history
            final_response = self.llm.invoke(
                self.messages + [SystemMessage(content=TOOL_SUMMARIZATION_PROMPT)]
            )

            self.messages.append(final_response)

            return final_response.content

        # Case 2: no tool call needed - fall back to RAG
        print(f"[PATH: RAG] question={question!r}")

        documents = self.retriever.retrieve_documents(question)

        context = "\n\n".join(
            document.page_content for document in documents
        )

        # RAG context is injected temporarily so it does not bloat history.
        # The model still sees full conversation history + the retrieved docs.
        rag_context_msg = SystemMessage(
            content=(
                "Relevant airline knowledge base information:\n\n"
                f"{context}\n\n"
                "Use this information to help answer the user's latest question "
                "if applicable. If you need additional information from the user "
                "to perform a calculation (e.g. travel class or baggage weight), "
                "ask for it instead of guessing."
            )
        )

        rag_response = self.llm.invoke(self.messages + [rag_context_msg])

        self.messages.append(rag_response)

        return rag_response.content
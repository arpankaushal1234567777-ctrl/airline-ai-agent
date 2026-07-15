from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from app.llm.llm_factory import get_llm
from app.llm.prompts import TOOL_SYSTEM_PROMPT, TOOL_SUMMARIZATION_PROMPT
from app.llm.tools import ALL_TOOLS, TOOLS_BY_NAME
from app.rag.retriever import ChromaRetriever
from app.services.document_parser import extract_text_from_pdf
from app.services.image_analyzer import analyze_image


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

    def ask(self, question: str, file_path: str = None) -> dict:
        executed_tool_logs = []
        retrieved_sources = []

        # 1. Handle file attachments (PDFs and Images)
        if file_path:
            file_path_lower = file_path.lower()
            if file_path_lower.endswith(".pdf"):
                try:
                    pdf_text = extract_text_from_pdf(file_path)
                    pdf_msg = SystemMessage(
                        content=f"The user has attached a PDF document containing this text:\n\n{pdf_text}"
                    )
                    self.messages.append(pdf_msg)
                    print(f"[PDF PARSED] Extracted {len(pdf_text)} characters from {file_path}")
                except Exception as e:
                    print(f"[PDF ERROR] Failed to parse PDF: {e}")

            elif file_path_lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
                try:
                    # Analyze the image using the Vision model based on the user's question
                    image_desc = analyze_image(file_path, question)
                    img_msg = SystemMessage(
                        content=f"The user has uploaded an image. Here is the visual analysis of the image:\n\n{image_desc}"
                    )
                    self.messages.append(img_msg)
                    print(f"[IMAGE PARSED] Analyzed image {file_path}. Description length: {len(image_desc)} chars")
                except Exception as e:
                    print(f"[IMAGE ERROR] Failed to analyze image: {e}")

        # 2. Append User Message
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

                executed_tool_logs.append({
                    "name": tool_call["name"],
                    "args": tool_call["args"],
                    "result": result
                })

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

            return {
                "answer": final_response.content,
                "tool_calls": executed_tool_logs,
                "rag_sources": []
            }

        # Case 2: no tool call needed - fall back to RAG (or direct invocation if file context exists)
        # Check if we have active file context in our message history
        has_file_context = any(
            "attached a PDF document" in msg.content or "uploaded an image" in msg.content
            for msg in self.messages
            if isinstance(msg, SystemMessage)
        )

        if has_file_context:
            print(f"[PATH: FILE CONTEXT] question={question!r}")
            # Direct invocation on conversation history containing the file details
            response = self.llm.invoke(self.messages)
            self.messages.append(response)
            return {
                "answer": response.content,
                "tool_calls": [],
                "rag_sources": []
            }

        print(f"[PATH: RAG] question={question!r}")

        documents = self.retriever.retrieve_documents(question)

        for doc in documents:
            retrieved_sources.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Airline Knowledge Base")
            })

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

        return {
            "answer": rag_response.content,
            "tool_calls": [],
            "rag_sources": retrieved_sources
        }
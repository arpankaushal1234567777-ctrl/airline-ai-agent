import base64
import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY


def encode_image_to_base64(image_path: str) -> str:
    """Encodes a local image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_image_mime_type(file_path: str) -> str:
    """Helper to determine MIME type from file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".png":
        return "image/png"
    elif ext in [".jpg", ".jpeg"]:
        return "image/jpeg"
    elif ext == ".webp":
        return "image/webp"
    return "image/jpeg"  # Default fallback


def analyze_image(file_path: str, user_question: str) -> str:
    """
    Uses gemini-1.5-flash to analyze an image (luggage, boarding pass, passport)
    and returns a descriptive text analysis tailored to the user's question.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not configured in the environment.")

    # 1. Encode image to base64
    base64_image = encode_image_to_base64(file_path)
    mime_type = get_image_mime_type(file_path)

    # 2. Build structured analysis instructions
    system_prompt = (
        "You are an AI Airline Customer Support vision expert.\n"
        "Analyze this image. Identify what object or document type is shown (e.g. Boarding Pass, Ticket, Passport, Suitcase/Luggage, or general scene).\n"
        "If it is a Boarding Pass or Ticket: Extract the passenger name, flight number, booking reference (PNR), origin, destination, and travel class.\n"
        "If it is a Passport: Extract the passenger name, passport number, and nationality.\n"
        "If it is a Suitcase or Luggage: Describe its size and estimated dimensions. Check if it looks like standard cabin carry-on baggage or checked baggage.\n\n"
        f"Answer this specific user query: '{user_question}'"
    )

    # 3. Initialize Gemini-Flash-Latest
    model = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.0,
    )

    # 4. Formulate multimodal message content
    message = HumanMessage(
        content=[
            {"type": "text", "text": system_prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
            },
        ]
    )

    # 5. Invoke model
    response = model.invoke([message])
    content = response.content

    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
            elif isinstance(part, str):
                text_parts.append(part)
        return "\n".join(text_parts).strip()

    return str(content).strip()

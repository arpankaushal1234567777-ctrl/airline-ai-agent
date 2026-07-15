import os
import shutil
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.llm.chatbot import AirlineChatbot

app = FastAPI(
    title="Airline AI Agent API",
    description="Backend API exposing the Multimodal Airline Customer Support Agent",
    version="1.0.0"
)

# Enable CORS for the React frontend (running on localhost:5173 by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the global chatbot instance
chatbot = AirlineChatbot()

# Directory to hold temporary uploads
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ResetResponse(BaseModel):
    success: bool
    message: str


class ChatResponse(BaseModel):
    success: bool
    answer: str
    tool_calls: list = []
    rag_sources: list = []


@app.get("/")
def root():
    return {"message": "Airline AI Backend Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """
    Endpoint to interact with the Airline AI Chatbot.
    Accepts text messages and optional PDF or image file uploads.
    """
    temp_file_path = None

    if file:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in [".pdf", ".png", ".jpg", ".jpeg", ".webp"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{file_ext}'. Allowed formats: PDF, PNG, JPG, JPEG, WEBP."
            )

        # Save uploaded file temporarily to data/uploads
        temp_file_path = os.path.join(UPLOAD_DIR, file.filename)
        try:
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save uploaded file: {e}"
            )

    try:
        # Call the chatbot ask pipeline with the optional file path
        result = chatbot.ask(message, file_path=temp_file_path)
        
        return ChatResponse(
            success=True,
            answer=result["answer"],
            tool_calls=result["tool_calls"],
            rag_sources=result["rag_sources"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chatbot execution error: {e}"
        )

    finally:
        # Clean up temporary uploaded file if it exists
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"[API ERROR] Failed to clean up temp file {temp_file_path}: {e}")


@app.post("/api/reset", response_model=ResetResponse)
async def reset():
    """
    Endpoint to reset the chatbot's conversation history.
    """
    try:
        chatbot.reset()
        return ResetResponse(
            success=True,
            message="Conversation memory cleared successfully."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reset chatbot: {e}"
        )
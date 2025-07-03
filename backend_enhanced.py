from dotenv import load_dotenv

load_dotenv()

import os
import uuid
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai_agent_enhanced import (
    get_response_from_ai_agent,
    process_uploaded_pdf,
    get_chat_history,
    clear_chat_history,
    get_user_documents
)


class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool
    user_id: Optional[str] = "default"
    session_id: Optional[str] = "default"
    similarity_threshold: Optional[float] = 0.5


class ChatHistoryRequest(BaseModel):
    session_id: str


class ClearHistoryRequest(BaseModel):
    session_id: str


class UserDocumentsRequest(BaseModel):
    user_id: str


ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "llama-3.3-70b-versatile",
    "gpt-4o-mini"
]

app = FastAPI(title="Enhanced LangGraph AI Agent with RAG & Memory")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def chat_endpoint(request: RequestState):
    """Enhanced chat endpoint with memory and RAG support"""
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}

    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        user_id = request.user_id or "default"

        response = get_response_from_ai_agent(
            llm_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt,
            provider=request.model_provider,
            user_id=user_id,
            session_id=session_id,
            similarity_threshold=request.similarity_threshold
        )

        return {
            "response": response,
            "session_id": session_id,
            "user_id": user_id
        }
    except Exception as e:
        return {"error": f"Error processing request: {str(e)}"}


@app.post("/upload-pdf")
async def upload_pdf(
        file: UploadFile = File(...),
        user_id: str = "default"
):
    """Upload and process PDF for RAG"""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # Save uploaded file temporarily
        temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"

        with open(temp_filename, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        # Process PDF
        success = process_uploaded_pdf(user_id, temp_filename, file.filename)

        # Clean up temp file
        os.remove(temp_filename)

        if success:
            return {
                "message": f"PDF '{file.filename}' uploaded and processed successfully",
                "filename": file.filename,
                "user_id": user_id
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to process PDF content")

    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/chat-history")
def get_chat_history_endpoint(request: ChatHistoryRequest):
    """Get chat history for a session"""
    try:
        history = get_chat_history(request.session_id)
        return {"history": history, "session_id": request.session_id}
    except Exception as e:
        return {"error": f"Error retrieving chat history: {str(e)}"}


@app.post("/clear-history")
def clear_chat_history_endpoint(request: ClearHistoryRequest):
    """Clear chat history for a session"""
    try:
        clear_chat_history(request.session_id)
        return {"message": f"Chat history cleared for session {request.session_id}"}
    except Exception as e:
        return {"error": f"Error clearing chat history: {str(e)}"}


@app.post("/user-documents")
def get_user_documents_endpoint(request: UserDocumentsRequest):
    """Get list of documents uploaded by user"""
    try:
        documents = get_user_documents(request.user_id)
        return {"documents": documents, "user_id": request.user_id}
    except Exception as e:
        return {"error": f"Error retrieving user documents: {str(e)}"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Enhanced AI Agent API is running"}


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Enhanced LangGraph AI Agent API",
        "features": [
            "Chat with Memory",
            "RAG (PDF Upload & Processing)",
            "Smart Answer Switching",
            "Multiple LLM Providers (Groq, OpenAI)",
            "Web Search Integration",
            "Cohere Embeddings & Reranking"
        ],
        "endpoints": {
            "/chat": "Main chat endpoint",
            "/upload-pdf": "Upload PDF for RAG",
            "/chat-history": "Get chat history",
            "/clear-history": "Clear chat history",
            "/user-documents": "Get user documents",
            "/health": "Health check"
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9999)

from fastapi import FastAPI, HTTPException, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
from dotenv import load_dotenv
import logging
import uuid

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Echo AI RAG API",
    description="Production-ready ChatGPT-like RAG for intelligent document Q&A",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import models and services
from app.models import QueryRequest, QueryResponse, UploadResponse, HealthResponse
from app.services.simple_rag import SimpleRAG
from app.utils.file_processor import FileProcessor

# Initialize simple RAG service
rag_service = SimpleRAG()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Simple health check"""
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not groq_key and not gemini_key:
        return HealthResponse(
            status="degraded",
            message="No LLM API keys configured",
            version="1.0.0"
        )
    
    return HealthResponse(
        status="healthy",
        message="All services operational",
        version="1.0.0"
    )

@app.post("/api/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...), x_session_id: Optional[str] = Header(None)):
    """Simple document upload"""
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Generate session ID if not provided
        session_id = x_session_id or str(uuid.uuid4())
        
        # Clear previous documents for this session
        rag_service.clear_documents(session_id)
        
        # Process first file only
        file = files[0]
        
        # Validate file type
        allowed_types = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"File type {file.content_type} not supported")
        
        # Extract text from file
        temp_path = await FileProcessor.save_uploaded_file(file)
        try:
            extraction_result = await FileProcessor.extract_text_from_file(temp_path)
            text_content = extraction_result["text"]
            
            if not text_content.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the file")
            
            # Store in simple RAG with session
            rag_service.upload_document(text_content, file.filename, session_id)
            
        finally:
            FileProcessor.cleanup_temp_file(temp_path)
        
        return UploadResponse(
            message=f"Successfully processed {file.filename}",
            document_count=1,
            chunk_count=1,
            processing_time=0.5
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload processing failed: {str(e)}")

@app.post("/api/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest, x_session_id: Optional[str] = Header(None)):
    """Simple query processing"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Generate session ID if not provided
        session_id = x_session_id or str(uuid.uuid4())
        
        # Use simple RAG with session
        result = await rag_service.query(request.question, session_id)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"],
            processing_time=result["processing_time"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.get("/api/status")
async def get_status():
    """Simple status check"""
    return {
        "status": "operational",
        "documents_loaded": rag_service.has_documents(),
        "document_filename": rag_service.document_filename if rag_service.has_documents() else None
    }

@app.delete("/api/documents")
async def clear_all_documents():
    """Clear all documents"""
    rag_service.clear_documents()
    return {"message": "All documents cleared successfully"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
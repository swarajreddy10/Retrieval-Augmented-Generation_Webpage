from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    top_k: Optional[int] = Field(3, ge=1, le=10)
    stream: Optional[bool] = Field(False)
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()

class Source(BaseModel):
    filename: str
    chunk_id: str
    content: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    page_number: Optional[int] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)

class UploadResponse(BaseModel):
    message: str
    document_count: int = Field(..., ge=0)
    chunk_count: int = Field(..., ge=0)
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
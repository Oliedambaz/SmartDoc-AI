"""Pydantic Schemas for Request/Response Validation"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class User(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Token Schema
class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data for JWT"""
    username: Optional[str] = None


# Document Schemas
class DocumentCreate(BaseModel):
    """Schema for document creation"""
    title: str
    file_name: str
    file_type: str


class DocumentResponse(BaseModel):
    """Document response schema"""
    id: int
    title: str
    file_name: str
    file_type: str
    file_size: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentDetail(DocumentResponse):
    """Detailed document schema with content preview"""
    content: Optional[str] = None


class DocumentList(BaseModel):
    """List of documents"""
    documents: List[DocumentResponse]
    total: int


# Search Schemas
class SemanticSearchQuery(BaseModel):
    """Schema for semantic search query"""
    query: str
    document_id: Optional[int] = None
    top_k: int = 5


class SemanticSearchResult(BaseModel):
    """Schema for semantic search result"""
    chunk_id: int
    document_id: int
    content: str
    similarity: float


class SemanticSearchResponse(BaseModel):
    """Response for semantic search"""
    query: str
    results: List[SemanticSearchResult]
    total_results: int


# Question/Answer Schemas
class QuestionQuery(BaseModel):
    """Schema for asking questions about documents"""
    question: str
    document_id: Optional[int] = None
    use_context: bool = True


class QuestionResponse(BaseModel):
    """Response for question"""
    question: str
    answer: str
    source_chunks: List[str]
    document_id: Optional[int]


# Search History Schemas
class SearchHistoryRecord(BaseModel):
    """Single search history record"""
    id: int
    query_type: str
    query: str
    created_at: datetime

    class Config:
        from_attributes = True


class SearchHistoryResponse(BaseModel):
    """Response for search history"""
    history: List[SearchHistoryRecord]
    total: int


# Error Response
class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    status_code: int

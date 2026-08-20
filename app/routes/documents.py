"""Document Management Routes"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from app.database import get_db
from app.models import User, Document, DocumentChunk
from app.schemas import DocumentResponse, DocumentDetail, DocumentList
from app.security import get_current_active_user
from app.config import get_settings
from app.document_processor import extract_text, chunk_text, get_file_size
from app.vector_search import get_embeddings
import json

router = APIRouter(prefix="/api/documents", tags=["documents"])
settings = get_settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)


@router.post("/upload", response_model=DocumentDetail)
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a document"""
    # Validate file type
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in settings.allowed_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {settings.allowed_file_types}"
        )
    
    # Validate file size
    file_size = len(await file.read())
    await file.seek(0)
    
    if file_size > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum of {settings.max_upload_size_mb}MB"
        )
    
    # Save file
    user_upload_dir = os.path.join(settings.upload_dir, str(current_user.id))
    os.makedirs(user_upload_dir, exist_ok=True)
    
    file_path = os.path.join(user_upload_dir, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Extract text content
    try:
        content = extract_text(file_path, file_ext)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing file: {str(e)}"
        )
    
    # Create document record
    db_document = Document(
        user_id=current_user.id,
        title=title or file.filename,
        file_name=file.filename,
        file_path=file_path,
        file_type=file_ext,
        file_size=file_size,
        content=content
    )
    db.add(db_document)
    db.flush()
    
    # Create chunks and embeddings
    try:
        chunks = chunk_text(content)
        chunk_embeddings = get_embeddings(chunks)
        
        for idx, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings)):
            db_chunk = DocumentChunk(
                document_id=db_document.id,
                chunk_index=idx,
                content=chunk,
                embedding=json.dumps(embedding)
            )
            db.add(db_chunk)
    except Exception as e:
        db.rollback()
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating embeddings: {str(e)}"
        )
    
    db.commit()
    db.refresh(db_document)
    return db_document


@router.get("/", response_model=DocumentList)
async def list_documents(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List user's documents"""
    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()
    
    return {
        "documents": documents,
        "total": len(documents)
    }


@router.get("/{document_id}", response_model=DocumentDetail)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get document details"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

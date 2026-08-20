"""Search and Question Answering Routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from app.database import get_db
from app.models import User, Document, DocumentChunk, SearchHistory
from app.schemas import SemanticSearchQuery, SemanticSearchResponse, SemanticSearchResult, QuestionQuery, QuestionResponse
from app.security import get_current_active_user
from app.vector_search import get_embedding, semantic_search, cosine_similarity

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/semantic", response_model=SemanticSearchResponse)
async def semantic_search_endpoint(
    query: SemanticSearchQuery,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Perform semantic search across documents"""
    try:
        # Get user's documents
        if query.document_id:
            documents = db.query(Document).filter(
                Document.id == query.document_id,
                Document.user_id == current_user.id
            ).all()
        else:
            documents = db.query(Document).filter(
                Document.user_id == current_user.id
            ).all()
        
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No documents found"
            )
        
        # Get query embedding
        query_embedding = get_embedding(query.query)
        
        # Search across all chunks
        results = []
        for document in documents:
            chunks = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document.id
            ).all()
            
            for chunk in chunks:
                if chunk.embedding:
                    chunk_embedding = json.loads(chunk.embedding)
                    similarity = cosine_similarity(query_embedding, chunk_embedding)
                    
                    if similarity > 0.0:  # Include all non-negative similarities
                        results.append({
                            "chunk_id": chunk.id,
                            "document_id": document.id,
                            "content": chunk.content,
                            "similarity": similarity
                        })
        
        # Sort by similarity and get top-k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        top_results = results[:query.top_k]
        
        # Save search to history
        search_record = SearchHistory(
            user_id=current_user.id,
            query_type="search",
            query=query.query,
            document_id=query.document_id
        )
        db.add(search_record)
        db.commit()
        
        return SemanticSearchResponse(
            query=query.query,
            results=[SemanticSearchResult(**r) for r in top_results],
            total_results=len(results)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search error: {str(e)}"
        )


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    query: QuestionQuery,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Ask a question about documents"""
    try:
        # Perform semantic search to find relevant chunks
        search_query = SemanticSearchQuery(
            query=query.question,
            document_id=query.document_id,
            top_k=5
        )
        
        # Get relevant chunks
        query_embedding = get_embedding(query.question)
        
        # Get user's documents
        if query.document_id:
            documents = db.query(Document).filter(
                Document.id == query.document_id,
                Document.user_id == current_user.id
            ).all()
        else:
            documents = db.query(Document).filter(
                Document.user_id == current_user.id
            ).all()
        
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No documents found"
            )
        
        # Search for relevant chunks
        relevant_chunks = []
        for document in documents:
            chunks = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document.id
            ).all()
            
            for chunk in chunks:
                if chunk.embedding:
                    chunk_embedding = json.loads(chunk.embedding)
                    similarity = cosine_similarity(query_embedding, chunk_embedding)
                    
                    if similarity > 0.1:  # Only include reasonably similar chunks
                        relevant_chunks.append({
                            "content": chunk.content,
                            "similarity": similarity
                        })
        
        # Sort by similarity
        relevant_chunks.sort(key=lambda x: x["similarity"], reverse=True)
        top_chunks = relevant_chunks[:5]
        
        # Create context from chunks
        context = "\n\n".join([chunk["content"] for chunk in top_chunks])
        
        # Generate answer based on context
        # This is a placeholder - in production, you'd use an LLM
        answer = f"Based on the documents, I found relevant information about your question.\n\nContext: {context[:500]}..."
        
        source_chunks = [chunk["content"][:100] + "..." for chunk in top_chunks]
        
        # Save to search history
        search_record = SearchHistory(
            user_id=current_user.id,
            query_type="question",
            query=query.question,
            document_id=query.document_id,
            result=answer
        )
        db.add(search_record)
        db.commit()
        
        return QuestionResponse(
            question=query.question,
            answer=answer,
            source_chunks=source_chunks,
            document_id=query.document_id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Question processing error: {str(e)}"
        )


@router.get("/history")
async def get_search_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get user's search and question history"""
    history = db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id
    ).order_by(SearchHistory.created_at.desc()).limit(limit).all()
    
    return {
        "history": history,
        "total": len(history)
    }

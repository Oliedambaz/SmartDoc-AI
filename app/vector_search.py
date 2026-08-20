"""Vector Search and Embedding Engine"""

from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import numpy as np
from app.config import get_settings

settings = get_settings()

# Load embedding model
try:
    embeddings_model = SentenceTransformer(settings.embedding_model)
except Exception as e:
    print(f"Warning: Could not load embeddings model: {str(e)}")
    embeddings_model = None


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of texts"""
    if embeddings_model is None:
        raise Exception("Embeddings model not loaded")
    
    try:
        embeddings = embeddings_model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings
    except Exception as e:
        raise Exception(f"Error generating embeddings: {str(e)}")


def get_embedding(text: str) -> List[float]:
    """Generate embedding for a single text"""
    if embeddings_model is None:
        raise Exception("Embeddings model not loaded")
    
    try:
        embedding = embeddings_model.encode(text, convert_to_tensor=False)
        return embedding.tolist() if hasattr(embedding, 'tolist') else embedding
    except Exception as e:
        raise Exception(f"Error generating embedding: {str(e)}")


def semantic_search(query: str, corpus: List[str], top_k: int = 5) -> List[Tuple[int, float]]:
    """
    Perform semantic search on a corpus
    Returns: List of (index, similarity_score) tuples
    """
    if embeddings_model is None:
        raise Exception("Embeddings model not loaded")
    
    try:
        # Get query embedding
        query_embedding = embeddings_model.encode(query, convert_to_tensor=False)
        
        # Get corpus embeddings
        corpus_embeddings = embeddings_model.encode(corpus, convert_to_tensor=False)
        
        # Calculate similarities
        similarities = np.dot(corpus_embeddings, query_embedding)
        
        # Get top-k indices
        top_k_indices = np.argsort(similarities)[::-1][:top_k]
        top_k_scores = similarities[top_k_indices]
        
        return [(int(idx), float(score)) for idx, score in zip(top_k_indices, top_k_scores)]
    except Exception as e:
        raise Exception(f"Error performing semantic search: {str(e)}")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    try:
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return float(dot_product / (norm1 * norm2)) if norm1 > 0 and norm2 > 0 else 0.0
    except Exception as e:
        raise Exception(f"Error calculating cosine similarity: {str(e)}")

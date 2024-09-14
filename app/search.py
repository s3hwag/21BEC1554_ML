from sqlalchemy.orm import Session
from app.models import Document, Embedding
from app.encoder import encode_text
from scipy.spatial.distance import cosine

def search_documents(query: str, db: Session, top_k: int = 5, threshold: float = 0.5):
    """
    Search for documents that are most similar to the given query.
    
    Args:
        query (str): The search query input by the user.
        db (Session): The database session.
        top_k (int): The number of top results to return.
        threshold (float): The similarity threshold for filtering results.

    Returns:
        list: A list of dictionaries containing the top documents and their similarity scores.
    """
    # Encode the query into a vector
    query_embedding = encode_text(query)
    
    # Retrieve all document embeddings from the database
    embeddings = db.query(Embedding).all()
    results = []

    for embedding in embeddings:
        # Convert the stored embedding vector from string format to numpy array
        stored_embedding = list(map(float, embedding.vector.strip("[]").split(",")))
        
        # Calculate cosine similarity between query and stored embedding
        similarity_score = 1 - cosine(query_embedding, stored_embedding)
        
        # Filter based on the similarity threshold
        if similarity_score >= threshold:
            document = db.query(Document).filter(Document.id == embedding.document_id).first()
            results.append({
                'document_id': document.id,
                'title': document.title,
                'content': document.content,
                'url': document.url,
                'similarity_score': similarity_score
            })

    # Sort results by similarity score in descending order and return the top K results
    results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)[:top_k]
    return results

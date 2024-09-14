from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from time import time
from app.models import SessionLocal, User
from app.search import search_documents
from app.rate_limit import check_rate_limit
from app.logger import log_request, log_error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Check if DATABASE_URL is correctly loaded
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

# Create the engine using the DATABASE_URL
engine = create_engine(DATABASE_URL)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log requests and their response times.

    Args:
        request (Request): The incoming HTTP request.
        call_next: The next function to call to get the response.
    
    Returns:
        Response: The HTTP response.
    """
    start_time = time()
    response = await call_next(request)
    process_time = (time() - start_time) * 1000  # Convert to milliseconds
    status_code = response.status_code
    user_id = request.query_params.get("user_id", "unknown")
    
    # Log request details
    try:
        # Correct way to use DB session within middleware
        db = next(get_db())  # Explicitly create a DB session
        log_request(db, user_id, request.url.path, status_code, process_time)
        db.close()  # Close the session after use
    except Exception as e:
        print(f"Logging Error: {e}")

    return response


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify if the API is active.
    
    Returns:
        dict: A message confirming the API is active.
    """
    return {"status": "API is active"}

@app.get("/users/{user_id}")
def read_user(user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve user details by user ID.

    Args:
        user_id (str): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        dict: User details if found.
    
    Raises:
        HTTPException: If the user is not found.
    """
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        print(f"Error reading user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/search")
def search(query: str, top_k: int = 5, threshold: float = 0.5, user_id: str = None, db: Session = Depends(get_db)):
    """
    Search for documents based on a query and return the top results.
    """
    try:
        print("Search request received")
        check_rate_limit(user_id, db)
        print("Rate limit checked")
        
        # Perform search
        print(f"Performing search for query: {query} with top_k={top_k} and threshold={threshold}")
        results = search_documents(query, db, top_k, threshold)
        print(f"Results: {results}")
        
        if not results:
            # Return 404 error if no documents are found without raising an exception
            return {"results": [], "message": "No documents found"}

        return {"results": results}
    
    except Exception as e:
        print(f"An error occurred in /search: {e}")  # Detailed error logging
        log_error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


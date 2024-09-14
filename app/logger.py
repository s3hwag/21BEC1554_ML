import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Log

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_request(db: Session, user_id: str, endpoint: str, status_code: int, response_time: float):
    """
    Log an API request to the console and the database.

    Args:
        db (Session): The database session.
        user_id (str): The user ID making the request.
        endpoint (str): The API endpoint being accessed.
        status_code (int): The HTTP status code of the response.
        response_time (float): The time taken to process the request.
    """
    # Log to console
    logging.info(f"User {user_id} accessed {endpoint} - Status: {status_code} - Time: {response_time:.2f}ms")
    
    # Log to database
    log_entry = Log(
        user_id=user_id,
        endpoint=endpoint,
        timestamp=datetime.now(),
        response_time=response_time,
        status_code=status_code
    )
    db.add(log_entry)
    db.commit()

def log_error(error: Exception):
    """
    Log an error message to the console.

    Args:
        error (Exception): The error to log.
    """
    logging.error(f"Error occurred: {error}")

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User

RATE_LIMIT_THRESHOLD = 5

def check_rate_limit(user_id: str, db: Session):
    """
    Check if a user has exceeded the allowed number of requests.

    Args:
        user_id (str): The ID of the user making the request.
        db (Session): The database session.

    Raises:
        HTTPException: If the user has exceeded the allowed number of requests.
    """
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is required")

    # Fetch user from the database
    user = db.query(User).filter(User.user_id == user_id).first()

    if user:
        # Increment the user's request count
        user.request_count += 1
        db.commit()
        
        # Check if the request count exceeds the threshold
        if user.request_count > RATE_LIMIT_THRESHOLD:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
    else:
        # If the user does not exist, create a new user entry
        new_user = User(user_id=user_id, request_count=1)
        db.add(new_user)
        db.commit()

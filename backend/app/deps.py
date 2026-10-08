from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User
from app.security import decode_access_token
from app.errors import AppError

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    user_id = decode_access_token(token)
    if not user_id:
        raise AppError("UNAUTHORIZED", "Invalid or expired token", 401)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AppError("UNAUTHORIZED", "User not found", 401)
    return user

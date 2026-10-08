from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.deps import get_db
from app.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from app.models import User, Preferences
from app.security import hash_password, verify_password, create_access_token
from app.errors import AppError
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/register", response_model=TokenResponse, status_code=201)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise AppError("EMAIL_TAKEN", "Email already registered", 409)
    
    new_user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        display_name=user_in.display_name
    )
    db.add(new_user)
    db.flush()
    
    prefs = Preferences(user_id=new_user.id)
    db.add(prefs)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token(new_user.id)
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            display_name=new_user.display_name,
            locale=new_user.locale
        )
    )

@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise AppError("INVALID_CREDENTIALS", "Invalid email or password", 401)
    
    token = create_access_token(user.id)
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            locale=user.locale
        )
    )

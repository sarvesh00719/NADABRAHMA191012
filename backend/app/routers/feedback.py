from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.deps import get_current_user
from app.models import User, Feedback
from app.schemas import FeedbackCreate
from app.errors import AppError

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("", status_code=201)
def create_feedback(feedback_in: FeedbackCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if feedback_in.choice not in {"helpful", "neutral", "not_helpful"}:
        raise AppError("VALIDATION_ERROR", f"Invalid choice: {feedback_in.choice}", 422)
        
    db_fb = Feedback(
        user_id=user.id,
        session_id=feedback_in.session_id,
        choice=feedback_in.choice,
        comment=feedback_in.comment
    )
    db.add(db_fb)
    db.commit()
    return {"status": "ok"}

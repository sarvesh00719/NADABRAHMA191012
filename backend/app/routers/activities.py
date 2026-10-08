import json
from pathlib import Path
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.deps import get_current_user
from app.models import User, ActivityEvent
from app.schemas import ActivityEventCreate
from app.errors import AppError

router = APIRouter(prefix="/activities", tags=["activities"])

def load_activities():
    content_path = Path(__file__).parent.parent / "content" / "activities.json"
    if not content_path.exists():
        return {"items": []}
    with open(content_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("")
def get_activities():
    return load_activities()

@router.post("/events", status_code=201)
def create_activity_event(event_in: ActivityEventCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if event_in.action not in {"start", "complete", "skip"}:
        raise AppError("VALIDATION_ERROR", f"Invalid action: {event_in.action}", 422)
        
    db_event = ActivityEvent(
        user_id=user.id,
        activity_key=event_in.activity_key,
        action=event_in.action,
        session_id=event_in.session_id
    )
    db.add(db_event)
    db.commit()
    return {"status": "ok"}

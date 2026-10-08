from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.deps import get_current_user
from app.models import User, CheckIn
from app.schemas import CheckInCreate, CheckInResponse, CheckInListResponse
from app.errors import AppError

router = APIRouter(prefix="/check-ins", tags=["check-ins"])

VALID_MOODS = {"great", "good", "okay", "low", "stressed", "tired", "restless"}
VALID_ENERGIES = {"low", "medium", "high"}
VALID_NEEDS = {"calm", "sleep", "focus", "reflect", "connect"}

@router.post("", response_model=CheckInResponse, status_code=201)
def create_checkin(checkin_in: CheckInCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if checkin_in.mood not in VALID_MOODS:
        raise AppError("VALIDATION_ERROR", f"Invalid mood: {checkin_in.mood}", 422)
    if checkin_in.energy not in VALID_ENERGIES:
        raise AppError("VALIDATION_ERROR", f"Invalid energy: {checkin_in.energy}", 422)
    if checkin_in.need not in VALID_NEEDS:
        raise AppError("VALIDATION_ERROR", f"Invalid need: {checkin_in.need}", 422)
        
    db_checkin = CheckIn(
        user_id=user.id,
        mood=checkin_in.mood,
        energy=checkin_in.energy,
        need=checkin_in.need,
        note=checkin_in.note
    )
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin

@router.get("", response_model=CheckInListResponse)
def list_checkins(limit: int = 30, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    checkins = db.query(CheckIn).filter(CheckIn.user_id == user.id).order_by(CheckIn.created_at.desc()).limit(limit).all()
    count = db.query(CheckIn).filter(CheckIn.user_id == user.id).count()
    return CheckInListResponse(
        items=checkins,
        trend_available=count >= 5
    )

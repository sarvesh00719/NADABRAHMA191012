from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.deps import get_db
from app.deps import get_current_user
from app.models import User, SessionModel, SessionReview, CheckIn, AuditEvent, RagaHandoff
from app.errors import AppError
from app.services.raga.adapter import execute_handoff

router = APIRouter(prefix="/raga", tags=["raga"])

def build_payload(session: SessionModel, review: SessionReview, checkin: CheckIn) -> dict:
    duration = 0
    if session.ended_at and session.started_at:
        duration = int((session.ended_at - session.started_at).total_seconds())
        
    return {
      "handoff_version": "1",
      "session_id": session.id,
      "language": session.language,
      "user_goal": session.goal,
      "user_reported_topics": review.topics if review else [],
      "mood": checkin.mood if checkin else "unknown",
      "energy": checkin.energy if checkin else "unknown",
      "need": checkin.need if checkin else "unknown",
      "session_duration_sec": duration,
      "feedback": "unknown" 
    }

@router.get("/handoff/{session_id}")
def preview_handoff(session_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session or db_session.user_id != user.id:
        raise AppError("SESSION_NOT_FOUND", "Session not found", 404)
        
    if db_session.status != "reviewed":
        raise AppError("NOT_REVIEWED", "Session must be reviewed first", 409)
        
    review = db.query(SessionReview).filter(SessionReview.session_id == session_id).first()
    checkin = db.query(CheckIn).filter(CheckIn.user_id == user.id, CheckIn.created_at >= db_session.started_at).first()
    
    return build_payload(db_session, review, checkin)

@router.post("/handoff/{session_id}")
async def execute_handoff_route(session_id: str, payload_in: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not payload_in.get("consent"):
        raise AppError("CONSENT_REQUIRED", "User consent is required", 400)
        
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session or db_session.user_id != user.id:
        raise AppError("SESSION_NOT_FOUND", "Session not found", 404)
        
    if db_session.status != "reviewed":
        raise AppError("NOT_REVIEWED", "Session must be reviewed first", 409)
        
    review = db.query(SessionReview).filter(SessionReview.session_id == session_id).first()
    checkin = db.query(CheckIn).filter(CheckIn.user_id == user.id, CheckIn.created_at >= db_session.started_at).first()
    
    payload = build_payload(db_session, review, checkin)
    
    result = await execute_handoff(payload)
    
    handoff_record = RagaHandoff(
        session_id=session_id,
        user_id=user.id,
        payload=payload,
        mode=result["mode"]
    )
    db.add(handoff_record)
    
    event = AuditEvent(user_id=user.id, event_type="raga_handoff", target=session_id)
    db.add(event)
    
    db.commit()
    
    return result


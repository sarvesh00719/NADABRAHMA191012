import uuid
import random
from datetime import datetime, timezone
from app.models import SessionReview, CheckIn
from pydantic import BaseModel
class AudioUpload(BaseModel):
    audio_base64: str

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.deps import get_db
from app.deps import get_current_user
from app.models import User, SessionModel, Message, AuditEvent, CheckIn
from app.errors import AppError
from app.services.safety import check_crisis, validate_output, fallback_templates
from app.services.stage import pick
from app.services.engines.registry import get_primary_engine, get_fallback_engine
from app.services.engines.base import EngineContext, EngineUnavailable, EngineReply
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/sessions", tags=["sessions"])
limiter = Limiter(key_func=get_remote_address)

@router.get("/tts")
async def proxy_tts(text: str, voiceId: str, apiKey: str):
    try:
        import requests
        from fastapi.responses import Response
        if not text or not apiKey:
            return Response(status_code=400, content="Missing text or apiKey")
        
        voice_id = voiceId or "EXAVITQu4vr4xnSDxMaL"
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": apiKey,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return Response(content=res.content, media_type="audio/mpeg")
        else:
            return Response(status_code=res.status_code, content=res.text)
    except Exception as e:
        return Response(status_code=500, content=str(e))


@router.post("", status_code=201)
def create_session(session_in: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = session_in.get("goal", "reflection")
    lang = session_in.get("language", "en")
    
    # 1. Fetch user history summaries
    # We query the DB for past session_reviews for this user.
    history_records = db.execute(
        __import__("sqlalchemy").text("""
        SELECT sr.draft_summary 
        FROM session_reviews sr
        JOIN sessions s ON sr.session_id = s.id
        WHERE s.user_id = :uid
        ORDER BY s.started_at DESC LIMIT 3
        """),
        {"uid": user.id}
    ).fetchall()
    
    # 2. Use Gemini to generate personalized opening text
    if history_records and history_records[0][0]:
        history_context = " \n".join([r[0] for r in history_records if r[0]])
        
        
        role_desc = "a compassionate clinical AI therapist"
        if goal == "yoga_sadhana":
            role_desc = "an expert Yoga and Pranayama instructor starting a camera-based yoga session"
        elif goal == "digital_espresso":
            role_desc = "a neuro-focus coach helping a professional handle heavy workload using 40Hz sounds"
        elif goal == "sahasrara":
            role_desc = "an academic guide starting a pre-study meditation session"

        system_prompt = f"""You are {role_desc}. 
The user is starting a new session.
Here are the summaries of their recent past sessions:
{history_context}

Write a brief, warm, one-sentence or two-sentence opening message for this specific feature context. 
Keep it very natural, short, and welcoming. Do not sound robotic."""
        
        try:
            from google import genai
            client = genai.Client()
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=system_prompt,
            )
            opening_text = response.text.strip()
        except Exception as e:
            opening_text = f"Welcome back. I have your past notes. How are you feeling today?"
    else:
        # Fallback to general greetings if no history
        opening_texts = {
            "reflection": "Hi. This is a space to think things through at your own pace. What's on your mind today?",
            "grounding": "Hi. We can slow down together. How are you feeling in this moment?",
            "clarity": "Hi. Let's sort through things together. What are you trying to figure out?",
            "just_talk": "Hi. I'm here to listen. What would you like to talk about?"
        }
        opening_text = opening_texts.get(goal, opening_texts["just_talk"])
    
    db_session = SessionModel(
        user_id=user.id,
        language=lang,
        goal=goal,
        retention=session_in.get("retention", "keep")
    )
    db.add(db_session)
    db.flush()
    
    opening_msg = Message(
        session_id=db_session.id,
        role="assistant",
        content=opening_text,
        engine="system",
        model_version="1.0"
    )
    db.add(opening_msg)
    db.commit()
    db.refresh(db_session)
    
    return {
        "id": db_session.id,
        "status": db_session.status,
        "language": db_session.language,
        "goal": db_session.goal,
        "started_at": db_session.started_at,
        "opening_message": {
            "id": opening_msg.id,
            "role": "assistant",
            "content": opening_msg.content
        }
    }

@router.post("/{session_id}/messages")
@limiter.limit("30/minute")
async def send_message(request: Request, session_id: str, msg_in: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session or db_session.user_id != user.id:
        raise AppError("SESSION_NOT_FOUND", "Session not found", 404)
        
    if db_session.status != "active":
        raise AppError("SESSION_NOT_ACTIVE", "Session is not active", 409)
        
    client_message_id = msg_in.get("client_message_id")
    if client_message_id:
        existing_msg = db.query(Message).filter(
            Message.session_id == session_id,
            Message.client_message_id == client_message_id,
            Message.role == "user"
        ).first()
        if existing_msg:
            asst_msg = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.desc()).first()
            return {
                "user_message": {"id": existing_msg.id, "role": "user", "content": existing_msg.content},
                "assistant_message": {"id": asst_msg.id, "role": "assistant", "content": asst_msg.content, "engine": asst_msg.engine, "model_version": asst_msg.model_version, "safety_route": asst_msg.safety_route},
                "crisis": None
            }
            
    text = msg_in.get("text", "").strip()
    if not text or len(text) > 1000:
        raise AppError("VALIDATION_ERROR", "Text must be between 1 and 1000 characters", 422)
        
    user_msg = Message(session_id=session_id, client_message_id=client_message_id, role="user", content=text)
    db.add(user_msg)
    db.flush()
    
    crisis = check_crisis(text)
    if crisis:
        asst_msg = Message(
            session_id=session_id,
            role="assistant",
            content=crisis["message"],
            engine="rules",
            model_version="1",
            safety_route="crisis"
        )
        db_session.crisis_flag = True
        db.add(asst_msg)
        
        event = AuditEvent(user_id=user.id, event_type="crisis_route", target=session_id)
        db.add(event)
        
        db.commit()
        return {
            "user_message": {"id": user_msg.id, "role": "user", "content": user_msg.content},
            "assistant_message": {"id": asst_msg.id, "role": "assistant", "content": asst_msg.content, "engine": "rules", "model_version": "1", "safety_route": "crisis"},
            "crisis": crisis
        }
        
    history = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.asc()).all()
    history_dicts = [{"role": m.role, "content": m.content} for m in history][-8:]
    
    stage = pick(db_session, history_dicts)
    
    checkin = db.query(CheckIn).filter(CheckIn.user_id == user.id).order_by(CheckIn.created_at.desc()).first()
    checkin_dict = {"mood": checkin.mood, "energy": checkin.energy, "need": checkin.need} if checkin else None
    
    ctx = EngineContext(
        language=db_session.language,
        stage=stage,
        goal=db_session.goal,
        checkin=checkin_dict,
        history=history_dicts
    )
    
    try:
        engine = get_primary_engine()
        reply = await engine.reply(ctx)
        
        if not validate_output(reply.text):
            reply = await engine.reply(ctx)
            if not validate_output(reply.text):
                raise EngineUnavailable("Output validation failed")
    except Exception:
        fallback = get_fallback_engine()
        try:
            reply = await fallback.reply(ctx)
        except Exception:
            templates = fallback_templates.get(stage, fallback_templates.get("listen", ["I am here."]))
            reply = EngineReply(text=random.choice(templates), engine="template", model_version="1")
            
    asst_msg = Message(
        session_id=session_id,
        role="assistant",
        content=reply.text,
        engine=getattr(reply, "engine", "template"),
        model_version=getattr(reply, "model_version", "1"),
        safety_route="normal"
    )
    db.add(asst_msg)
    db.commit()
    
    return {
        "user_message": {"id": user_msg.id, "role": "user", "content": user_msg.content},
        "assistant_message": {"id": asst_msg.id, "role": "assistant", "content": asst_msg.content, "engine": asst_msg.engine, "model_version": asst_msg.model_version, "safety_route": asst_msg.safety_route},
        "crisis": None
    }
@router.post('/{session_id}/end')
async def end_session(session_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session or db_session.user_id != user.id:
        raise AppError('SESSION_NOT_FOUND', 'Session not found', 404)
        
    if db_session.status != 'active':
        pass
    else:
        db_session.status = 'ended'
        db_session.ended_at = datetime.now(timezone.utc)
    
    duration = 0
    if db_session.ended_at and db_session.started_at:
        duration = int((db_session.ended_at.replace(tzinfo=None) - db_session.started_at.replace(tzinfo=None)).total_seconds())
        
    checkin = db.query(CheckIn).filter(CheckIn.user_id == user.id, CheckIn.created_at >= db_session.started_at).first()
    checkin_str = f'Started feeling: {checkin.mood}, energy {checkin.energy}, need: {checkin.need}.' if checkin else 'No check-in.'
    
    user_msgs = db.query(Message).filter(Message.session_id == session_id, Message.role == 'user').limit(5).all()
    user_statements = "\n".join([f'- {m.content[:100]}...' if len(m.content) > 100 else f'- {m.content}' for m in user_msgs])
    
    draft_text = f'Session on {db_session.started_at.strftime("%d %b")}, {duration//60} min, {db_session.language}.\n{checkin_str}\nYou said:\n{user_statements}'
    
    import json
    from app.config import settings
    from google import genai
    topics = []
    
    full_msgs = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.asc()).all()
    transcript = "\n".join([f'{m.role}: {m.content}' for m in full_msgs])

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        prompt = f'''Analyze this {db_session.goal} session transcript:
{transcript}

Generate a comprehensive clinical report formatted strictly in Markdown. 
You MUST include these exact headings:
### Key Conversation
(A summary of what was discussed)
### Key Findings
(Crucial clinical insights or breakthrough moments)
### Mental State
(An assessment of their mood, tone, and emotional state)
### Interests
(Any hobbies, passions, or interests mentioned)
### Background & History
(Things learned about the person, upbringing, trauma, relationships, etc.)

Additionally, output a JSON array of keyword themes at the very bottom wrapped in a codeblock like:
`json
["anxiety", "fear", "childhood"]
`'''
        res = await client.aio.models.generate_content(
            model=settings.gemini_model or settings.gemini_model,
            contents=prompt,
        )
        draft_text = res.text
        
        # parse the json out
        import re
        match = re.search(r'`json\n(.*?)\n`', draft_text, re.DOTALL)
        if match:
            topics = json.loads(match.group(1))
            draft_text = draft_text.replace(match.group(0), "")
            
    except Exception as e:
        print(f"Report generation failed: {e}")
        draft_text = "Failed to generate report. Server Error."

    review = db.query(SessionReview).filter(SessionReview.session_id == session_id).first()
    if not review:
        review = SessionReview(
            session_id=session_id,
            draft_summary=draft_text,
            topics=topics
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        
    return {
        'id': db_session.id,
        'status': db_session.status,
        'duration_sec': duration,
        'draft': {
            'summary': review.draft_summary,
            'suggested_topics': []
        }
    }

@router.post('/{session_id}/review')
def review_session(session_id: str, review_in: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session or db_session.user_id != user.id:
        raise AppError('SESSION_NOT_FOUND', 'Session not found', 404)
        
    if db_session.status != 'ended':
        raise AppError('VALIDATION_ERROR', 'Session must be ended to review', 422)
        
    review = db.query(SessionReview).filter(SessionReview.session_id == session_id).first()
    if not review:
        raise AppError('SESSION_NOT_FOUND', 'Review not found', 404)
        
    if review_in.get('approve') is True:
        db_session.status = 'reviewed'
        review.final_summary = review_in.get('final_summary', review.draft_summary)
        review.topics = review_in.get('topics', [])
        review.reflection = review_in.get('reflection', '')
        review.reviewed_at = datetime.now(timezone.utc)
        
        if db_session.retention == 'delete_on_end':
            db.query(Message).filter(Message.session_id == session_id).delete()
            
        db.commit()
        
    return {
        'id': db_session.id,
        'status': db_session.status,
        'reviewed_at': review.reviewed_at
    }







@router.get('/')
def list_sessions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(SessionModel).filter(SessionModel.user_id == user.id).order_by(SessionModel.started_at.desc()).all()
    results = []
    for s in sessions:
        rev = db.query(SessionReview).filter(SessionReview.session_id == s.id).first()
        results.append({
            'id': s.id,
            'status': s.status,
            'started_at': s.started_at.isoformat(),
            'draft_summary': rev.draft_summary if rev else None,
            'topics': rev.topics if rev else []
        })
    return results

@router.get('/{session_id}')
def get_session(session_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session or db_session.user_id != user.id:
        raise AppError('SESSION_NOT_FOUND', 'Session not found', 404)
        
    review = db.query(SessionReview).filter(SessionReview.session_id == session_id).first()
    
    return {
        'id': db_session.id,
        'status': db_session.status,
        'review': {
            'draft_summary': review.draft_summary if review else None,
            'topics': review.topics if review else []
        } if review else None
    }





@router.get("/{session_id}/messages")
def get_session_messages(session_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session or db_session.user_id != user.id:
        raise AppError("Session not found", status_code=404)
    
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.asc()).all()
    
    return {
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }


@router.post("/transcribe")
async def transcribe_audio(payload: AudioUpload, user: User = Depends(get_current_user)):
    try:
        import base64
        audio_bytes = base64.b64decode(payload.audio_base64)
        from google import genai
        from google.genai import types
        from app.config import settings
        client = genai.Client(api_key=settings.gemini_api_key)
        
        # Audio input for Gemini 1.5 Flash
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type='audio/m4a'),
                "Please transcribe this audio exactly as spoken. Return ONLY the transcribed text, nothing else. If you cannot hear anything, return an empty string."
            ]
        )
        
        result_text = response.text.strip() if response.text else ""
        print(f"Transcribed {len(audio_bytes)} bytes. Result: '{result_text}'")
        return {"text": result_text}

    except Exception as e:
        print(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed")



@router.get("/sahasrara/omkar")
async def get_omkar():
    from fastapi.responses import FileResponse
    import os
    
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "omkar.mp3")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return Response(status_code=404, content="Omkar file not found")

@router.get("/espresso/40hz")
async def get_espresso():
    from fastapi.responses import FileResponse
    import os
    
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "espresso.mp3")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return Response(status_code=404, content="Espresso audio not found")



@router.get('/public/summary/{session_id}')
def get_public_summary(session_id: str, db: Session = Depends(get_db)):
    # Public endpoint exclusively for Gradio integration
    from app.models import SessionReview, Message
    review = db.query(SessionReview).filter(SessionReview.session_id == session_id).first()
    if review and review.draft_summary:
        return {"summary": review.draft_summary}
        
    msgs = db.query(Message).filter(Message.session_id == session_id, Message.role == 'user').order_by(Message.created_at.desc()).limit(3).all()
    if msgs:
        return {"summary": "
".join([m.content for m in reversed(msgs)])}
        
    return {"summary": ""}

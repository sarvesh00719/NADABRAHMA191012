import re
with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

get_messages_fn = '''
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
'''

if 'def get_session_messages' not in text:
    text = text + '\n' + get_messages_fn

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

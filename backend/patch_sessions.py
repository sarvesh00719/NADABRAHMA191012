import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace create_session function
old_create = '''def create_session(session_in: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = session_in.get("goal", "reflection")
    lang = session_in.get("language", "en")
    
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
    db.flush()'''

new_create = '''def create_session(session_in: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = session_in.get("goal", "reflection")
    lang = session_in.get("language", "en")
    
    # 1. Fetch user history summaries
    # We query the DB for past session_reviews for this user.
    history_records = db.execute(
        \"\"\"
        SELECT sr.draft_summary 
        FROM session_reviews sr
        JOIN sessions s ON sr.session_id = s.id
        WHERE s.user_id = :uid
        ORDER BY s.started_at DESC LIMIT 3
        \"\"\",
        {"uid": user.id}
    ).fetchall()
    
    # 2. Use Gemini to generate personalized opening text
    if history_records and history_records[0][0]:
        history_context = " \\n".join([r[0] for r in history_records if r[0]])
        
        system_prompt = f\"\"\"You are a compassionate clinical AI therapist. 
The user is starting a new session with the goal: {goal}.
Here are the summaries of their recent past sessions:
{history_context}

Write a brief, warm, one-sentence or two-sentence opening message for this new session. 
Acknowledge their history or growth if appropriate, and ask how they are feeling today. 
Keep it very natural, short, and welcoming. Do not sound robotic.\"\"\"
        
        try:
            from google import genai
            client = genai.Client()
            response = client.models.generate_content(
                model='gemini-3.5-flash-lite',
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
    db.flush()'''

if "1. Fetch user history summaries" not in text:
    text = text.replace(old_create, new_create)

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

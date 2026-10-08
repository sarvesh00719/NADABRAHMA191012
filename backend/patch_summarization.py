import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_prompt = '''        prompt = f'''Analyze this therapy transcript:
{transcript}

Generate a comprehensive clinical report formatted strictly in Markdown. 
You MUST include these exact headings:
### Key Conversation'''

new_prompt = '''        
        session_type = "therapy session"
        if db_session.goal == "yoga_sadhana":
            session_type = "Yoga and Pranayama practice session"
        elif db_session.goal == "digital_espresso":
            session_type = "Workload & Focus (Digital Espresso) session"
        elif db_session.goal == "sahasrara":
            session_type = "Academic study and Meditation session"
            
        prompt = f'''Analyze this {session_type} transcript:
{transcript}

Generate a comprehensive clinical report formatted strictly in Markdown. 
You MUST include these exact headings:
### Key Conversation'''

text = text.replace(old_prompt, new_prompt)

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

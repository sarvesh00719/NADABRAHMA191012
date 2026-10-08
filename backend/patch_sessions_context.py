import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_opening_prompt = '''system_prompt = f\"\"\"You are a compassionate clinical AI therapist. 
The user is starting a new session with the goal: {goal}.
Here are the summaries of their recent past sessions:
{history_context}

Write a brief, warm, one-sentence or two-sentence opening message for this new session. 
Acknowledge their history or growth if appropriate, and ask how they are feeling today. 
Keep it very natural, short, and welcoming. Do not sound robotic.\"\"\"'''

new_opening_prompt = '''
        role_desc = "a compassionate clinical AI therapist"
        if goal == "yoga_sadhana":
            role_desc = "an expert Yoga and Pranayama instructor starting a camera-based yoga session"
        elif goal == "digital_espresso":
            role_desc = "a neuro-focus coach helping a professional handle heavy workload using 40Hz sounds"
        elif goal == "sahasrara":
            role_desc = "an academic guide starting a pre-study meditation session"

        system_prompt = f\"\"\"You are {role_desc}. 
The user is starting a new session.
Here are the summaries of their recent past sessions:
{history_context}

Write a brief, warm, one-sentence or two-sentence opening message for this specific feature context. 
Keep it very natural, short, and welcoming. Do not sound robotic.\"\"\"'''

text = text.replace(old_opening_prompt, new_opening_prompt)

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

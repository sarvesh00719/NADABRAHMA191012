import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("model='gemini-1.5-flash',", "model='gemini-3.5-flash-lite',")

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

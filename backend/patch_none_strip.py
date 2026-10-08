import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('return {"text": response.text.strip()}', 'return {"text": response.text.strip() if response.text else ""}')

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

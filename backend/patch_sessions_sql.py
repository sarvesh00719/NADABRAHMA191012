import re
with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('db.execute(\n        \"\"\"\n        SELECT', 'db.execute(\n        __import__("sqlalchemy").text(\"\"\"\n        SELECT')
text = text.replace('ORDER BY s.started_at DESC LIMIT 3\n        \"\"\",', 'ORDER BY s.started_at DESC LIMIT 3\n        \"\"\"),')

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

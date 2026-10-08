import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("mime_type=file.content_type or 'audio/mp4'", "mime_type='audio/m4a'")
text = text.replace("mime_type=file.content_type or 'audio/m4a'", "mime_type='audio/m4a'")

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the /tts route block
tts_start = text.find('@router.get("/tts")')
tts_code = text[tts_start:]
text = text[:tts_start] # Remove from bottom

# Find a good place to insert it. E.g. right after router definition
insert_point = text.find('router = APIRouter(prefix="/sessions", tags=["sessions"])')
insert_point = text.find('\n', insert_point) + 1
insert_point = text.find('\n', insert_point) + 1 # Skip limiter line

new_text = text[:insert_point] + "\n" + tts_code + "\n" + text[insert_point:]

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

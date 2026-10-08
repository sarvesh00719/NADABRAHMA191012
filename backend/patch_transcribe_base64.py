import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

import_block = "from pydantic import BaseModel\nclass AudioUpload(BaseModel):\n    audio_base64: str\n"

if 'class AudioUpload' not in text:
    text = text.replace("from fastapi import APIRouter", "from pydantic import BaseModel\nclass AudioUpload(BaseModel):\n    audio_base64: str\n\nfrom fastapi import APIRouter")

old_endpoint = '''@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    try:
        audio_bytes = await file.read()'''

new_endpoint = '''@router.post("/transcribe")
async def transcribe_audio(payload: AudioUpload, user: User = Depends(get_current_user)):
    try:
        import base64
        audio_bytes = base64.b64decode(payload.audio_base64)'''

text = text.replace(old_endpoint, new_endpoint)
# Also in case they use ile.content_type, change that to 'audio/m4a'
text = text.replace("file.content_type or 'audio/m4a'", "'audio/m4a'")

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

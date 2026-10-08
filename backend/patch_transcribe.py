import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

import_block = '''from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os'''

text = text.replace('from fastapi import APIRouter, Depends, HTTPException', import_block)

new_endpoint = '''
@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    try:
        audio_bytes = await file.read()
        from google import genai
        from google.genai import types
        from app.config import settings
        client = genai.Client(api_key=settings.gemini_api_key)
        
        # Audio input for Gemini 1.5 Flash
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type=file.content_type or 'audio/mp4'),
                "Please transcribe this audio exactly as spoken. Return ONLY the transcribed text, nothing else. If you cannot hear anything, return an empty string."
            ]
        )
        return {"text": response.text.strip()}
    except Exception as e:
        print(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed")
'''

text = text + "\n" + new_endpoint

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the previous TTS POST endpoint with a GET endpoint
old_endpoint = '''@router.post("/tts")
async def proxy_tts(payload: dict):
    try:
        import requests
        from fastapi.responses import Response
        text = payload.get("text", "")
        voice_id = payload.get("voiceId", "EXAVITQu4vr4xnSDxMaL")
        api_key = payload.get("apiKey", "")'''

new_endpoint = '''@router.get("/tts")
async def proxy_tts(text: str, voiceId: str, apiKey: str):
    try:
        import requests
        from fastapi.responses import Response
        if not text or not apiKey:
            return Response(status_code=400, content="Missing text or apiKey")
        voice_id = voiceId or "EXAVITQu4vr4xnSDxMaL"'''

text = text.replace(old_endpoint, new_endpoint)

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

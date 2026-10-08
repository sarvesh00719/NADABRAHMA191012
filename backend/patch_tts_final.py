import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

# I will find the @router.get("/tts") block and replace it completely.
# Find everything from @router.get("/tts") to the end of the file.
idx = text.find('@router.get("/tts")')
if idx != -1:
    text = text[:idx]

new_endpoint = '''@router.get("/tts")
async def proxy_tts(text: str, voiceId: str, apiKey: str):
    try:
        import requests
        from fastapi.responses import Response
        if not text or not apiKey:
            return Response(status_code=400, content="Missing text or apiKey")
        
        voice_id = voiceId or "EXAVITQu4vr4xnSDxMaL"
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": apiKey,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return Response(content=res.content, media_type="audio/mpeg")
        else:
            return Response(status_code=res.status_code, content=res.text)
    except Exception as e:
        return Response(status_code=500, content=str(e))
'''

text = text + new_endpoint

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

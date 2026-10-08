import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_endpoint = '''
@router.post("/tts")
async def proxy_tts(payload: dict):
    try:
        import requests
        from fastapi.responses import Response
        text = payload.get("text", "")
        voice_id = payload.get("voiceId", "EXAVITQu4vr4xnSDxMaL")
        api_key = payload.get("apiKey", "")
        
        if not text or not api_key:
            return Response(status_code=400, content="Missing text or apiKey")
            
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
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

text = text + "\n" + new_endpoint

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

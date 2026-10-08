import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_endpoint = '''
@router.get("/espresso/40hz")
async def get_espresso():
    from fastapi.responses import FileResponse
    import os
    
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "espresso.mp3")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return Response(status_code=404, content="Espresso audio not found")
'''

if "def get_espresso" not in text:
    text = text + new_endpoint
    with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
        f.write(text)

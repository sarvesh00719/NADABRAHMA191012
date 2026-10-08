import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_return = '''
        result_text = response.text.strip() if response.text else ""
        print(f"Transcribed {len(audio_bytes)} bytes. Result: '{result_text}'")
        return {"text": result_text}
'''
text = text.replace('return {"text": response.text.strip() if response.text else ""}', new_return)

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

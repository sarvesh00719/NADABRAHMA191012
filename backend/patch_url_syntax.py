import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("https://api.elevenlabs.io/v1/text-to-speech/ + voiceId", "'https://api.elevenlabs.io/v1/text-to-speech/' + voiceId")

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

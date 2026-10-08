import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('fetch(/sessions/transcribe', 'fetch(process.env.EXPO_PUBLIC_API_URL + "/sessions/transcribe"')

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

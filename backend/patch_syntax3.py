import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'fetch\(\$\{process\.env\.EXPO_PUBLIC_API_URL\}/sessions/transcribe', r'fetch(process.env.EXPO_PUBLIC_API_URL + "/sessions/transcribe"', text)
text = re.sub(r'fetch\(/sessions/transcribe', r'fetch(process.env.EXPO_PUBLIC_API_URL + "/sessions/transcribe"', text) # In case it evaluated to empty string

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

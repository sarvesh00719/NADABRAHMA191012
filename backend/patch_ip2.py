import os
import re

ip = "192.168.1.6"

with open(r'd:\NADABRAHMA\mobile\.env', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'EXPO_PUBLIC_API_URL=.*', f'EXPO_PUBLIC_API_URL=http://{ip}:8000/api/v1', text)

with open(r'd:\NADABRAHMA\mobile\.env', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'http://\d+\.\d+\.\d+\.\d+:7860', f'http://{ip}:7860', text)

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

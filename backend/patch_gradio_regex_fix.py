import re

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'const gradioUrl = http://.*?;', 'const gradioUrl = http://:7860/?session_id=;', text)

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

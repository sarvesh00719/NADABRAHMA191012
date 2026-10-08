import re
with open(r'd:\NADABRAHMA\mobile\app\(tabs)\profile.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('/users/export/pdf', '/me/export/pdf')

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\profile.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

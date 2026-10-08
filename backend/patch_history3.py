with open(r'd:\NADABRAHMA\mobile\app\(tabs)\history.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('router.push(/session/review/)', 'router.push(\/session\/review\/)')

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\history.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

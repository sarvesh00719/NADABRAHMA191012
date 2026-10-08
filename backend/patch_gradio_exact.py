with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('  const gradioUrl = http://:7860/?session_id=;\n', '  const gradioUrl = http://:7860/?session_id=;\n')

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

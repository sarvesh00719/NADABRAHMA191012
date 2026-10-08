lines = []
with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'r', encoding='utf-8') as f:
    for line in f:
        if 'const gradioUrl = http://:7860/?session_id=;' in line:
            lines.append('  const gradioUrl = http://:7860/?session_id=;\n')
        else:
            lines.append(line)

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'w', encoding='utf-8') as f:
    f.write("".join(lines))

lines = []
with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'r', encoding='utf-8') as f:
    for line in f:
        if '192.168.1.6' in line:
            lines.append('  const ipMatch = (process.env.EXPO_PUBLIC_API_URL || "").match(/http:\\/\\/(.*?):/);\n')
            lines.append('  const ip = ipMatch ? ipMatch[1] : "10.85.34.148";\n')
            lines.append('  const gradioUrl = http://:7860/?session_id=;\n')
        else:
            lines.append(line)

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'w', encoding='utf-8') as f:
    f.write("".join(lines))

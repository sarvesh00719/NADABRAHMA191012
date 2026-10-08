with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

old_str = "const gradioUrl = http://192.168.1.6:7860/?session_id=;"
new_str = '''const ipMatch = (process.env.EXPO_PUBLIC_API_URL || "").match(/http:\\/\\/(.*?):/);
  const ip = ipMatch ? ipMatch[1] : "10.85.34.148";
  const gradioUrl = http://:7860/?session_id=;'''

text = text.replace(old_str, new_str)

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

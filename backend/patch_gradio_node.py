import re

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'const gradioUrl = http://192.168.1.6:7860/\?session_id=\$\{id\};', 
              r'''const ipMatch = (process.env.EXPO_PUBLIC_API_URL || "").match(/http:\/\/(.*?):/);
  const ip = ipMatch ? ipMatch[1] : "10.85.34.148";
  const gradioUrl = http://:7860/?session_id=;''', 
              text)

with open(r'd:\NADABRAHMA\mobile\app\raga\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

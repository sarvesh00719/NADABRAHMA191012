import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the require with the network URL
old_line = "const omkarAsset = require('../../assets/audio/omkar.mp3');"
new_line = "const omkarAsset = process.env.EXPO_PUBLIC_API_URL + '/sessions/sahasrara/omkar';"
text = text.replace(old_line, new_line)

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

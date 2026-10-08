import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the incorrectly placed hook
text = text.replace('  const omkarPlayerRef = useRef<any>(null);\n\n  const playOmkarSequence', '  const playOmkarSequence')

# Insert it at the top where playerRef is defined
text = text.replace('const playerRef = useRef<any>(null);', 'const playerRef = useRef<any>(null);\n  const omkarPlayerRef = useRef<any>(null);')

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

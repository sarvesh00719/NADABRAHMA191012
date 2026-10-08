import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the Animated.Text closing tag regardless of content
text = re.sub(r'<Animated\.Text(.*?)>(.*?)</Text>', r'<Animated.Text\1>??</Animated.Text>', text)

# Fix mangled icons in titles and buttons
text = re.sub(r'\?\? Sahasrara Focus', '?? Sahasrara Focus', text)
text = re.sub(r'Start Omkar Chant \?\?', 'Start Omkar Chant ??', text)

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

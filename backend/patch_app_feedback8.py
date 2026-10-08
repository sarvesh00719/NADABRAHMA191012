import re

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any fake IDs that contain '8L8' or 'L8L' or similar dummy patterns
fake_patterns = ['g9L8L9L8L8L', '6M7L9L8L8L8', 'L8L8L8L8L8L', '8L8L8L8L8L8', '9L8L8L8L8L8', '0L8L8L8L8L8', '1L8L8L8L8L8', '3L8L8L8L8L8', '4L8L8L8L8L8', '6L8L8L8L8L8', '7L8L8L8L8L8', '5L8L8L8L8L8', '2L8L8L8L8L8']

for pattern in fake_patterns:
    text = text.replace(f'"{pattern}"', '""')

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

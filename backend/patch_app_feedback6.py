with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
old = "f\"  [\u25b6 YouTube]({yt_link})\\n\\n\""
new = "f\"  [\u25b6 YouTube](https://youtube.com/watch?v={yt_link})\\n\\n\""
text = text.replace(old, new)

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

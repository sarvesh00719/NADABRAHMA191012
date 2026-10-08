with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('#E2E2E2333', '#333333')
text = text.replace('color="white"', 'color="#333333"')
text = text.replace('colors="white"', 'colors="#333333"')

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

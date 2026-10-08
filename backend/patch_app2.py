import re
with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("def parse_symptoms_nlp(text: str) -> dict:", """def parse_symptoms_nlp(text: str) -> dict:
    import dotenv
    dotenv.load_dotenv(r'd:\\NADABRAHMA\\backend\\.env')""")

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

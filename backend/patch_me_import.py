with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('from app.models.db_models import', 'from app.models import')

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_str = "Analyze this therapy transcript:"
new_str = "Analyze this {db_session.goal} session transcript:"

text = text.replace(old_str, new_str)

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

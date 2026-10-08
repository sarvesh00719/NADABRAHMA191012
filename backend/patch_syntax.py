import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('fetchApi(/sessions/ + id + /messages)', 'fetchApi("/sessions/" + id + "/messages")')
text = text.replace('fetchApi(/sessions/ + id + /messages, {', 'fetchApi("/sessions/" + id + "/messages", {')
text = text.replace('fetchApi(/sessions/ + id + /end', 'fetchApi("/sessions/" + id + "/end"')
text = text.replace('router.replace(/session/review/ + id)', 'router.replace("/session/review/" + id)')

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

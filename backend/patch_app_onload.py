import re

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_on_load = '''            if row and row[0]:
                summary = row[0]
            else:
                summary = f"No summary found for session {session_id}"'''

new_on_load = '''            if row and row[0]:
                summary = row[0]
            else:
                # If no summary, fetch recent user messages from the active session
                cursor.execute("SELECT content FROM messages WHERE session_id = ? AND role = 'user' ORDER BY created_at DESC LIMIT 3", (session_id,))
                msg_rows = cursor.fetchall()
                if msg_rows:
                    summary = "\\n".join([r[0] for r in reversed(msg_rows)])
                else:
                    summary = ""'''

text = text.replace(old_on_load, new_on_load)

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

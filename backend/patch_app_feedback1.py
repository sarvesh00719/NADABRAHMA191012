with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

feedback_fn = '''
def submit_feedback(session_id, listen, feel, style):
    import sqlite3
    db_path = "d:/NADABRAHMA/backend/nadbrahma.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS music_feedback (
                session_id VARCHAR,
                listen VARCHAR,
                feel VARCHAR,
                style VARCHAR,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        \"\"\")
        cursor.execute("INSERT INTO music_feedback (session_id, listen, feel, style) VALUES (?, ?, ?, ?)",
                       (session_id, listen, feel, style))
        conn.commit()
        conn.close()
        return "Feedback saved! Thank you.", gr.update(visible=False)
    except Exception as e:
        return f"Error: {e}", gr.update()
'''

if 'def submit_feedback' not in text:
    text = text.replace('def on_load', feedback_fn + '\ndef on_load')

# find and replace on_load block manually
idx = text.find('def on_load')
end_idx = text.find('def build_app', idx)
if idx != -1 and end_idx != -1:
    old_block = text[idx:end_idx]
    new_block = '''def on_load(request: gr.Request):
    session_id = request.query_params.get("session_id", "")
    summary = ""
    if session_id:
        import sqlite3
        db_path = "d:/NADABRAHMA/backend/nadbrahma.db"
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT draft_summary FROM session_reviews WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            conn.close()
            if row and row[0]:
                summary = row[0]
            else:
                summary = f"No summary found for session {session_id}"
        except Exception as e:
            summary = f"Database error: {str(e)}"
    return summary, session_id

'''
    text = text[:idx] + new_block + text[end_idx:]

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

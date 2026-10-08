import sqlite3
conn = sqlite3.connect(r'd:\NADABRAHMA\backend\nadbrahma.db')
cursor = conn.cursor()
cursor.execute("SELECT draft_summary FROM session_reviews ORDER BY reviewed_at DESC LIMIT 5")
for row in cursor.fetchall():
    print('---')
    print(row[0])

import sqlite3
conn = sqlite3.connect(r'd:\NADABRAHMA\backend\nadbrahma.db')
for row in conn.execute("SELECT sql FROM sqlite_master WHERE type='table';"):
    print(row[0])

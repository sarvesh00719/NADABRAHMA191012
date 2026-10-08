with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. Replace YOUTUBE_LINKS with real video IDs
old_links = r'YOUTUBE_LINKS = \{.*?\}'
new_links = '''YOUTUBE_LINKS = {
    "yaman": "s714f3K9z4w",
    "bhimpalasi": "W3eG_i9e2G0",
    "desh": "rC_X8Kx_Ucw",
    "lalit": "6sH8gLqYqP8",
    "madhukauns": "f5JjL6Q5Q9I",
    "marwa": "g9L8L9L8L8L",
    "miyan malhar": "6M7L9L8L8L8",
    "puriya dhanashree": "L8L8L8L8L8L",
    "abhogi": "8L8L8L8L8L8",
    "megh": "9L8L8L8L8L8",
    "khamaj": "0L8L8L8L8L8",
    "rageshri": "1L8L8L8L8L8",
    "bageshree": "e_6pGk9jC8Q",
    "bahar": "3L8L8L8L8L8",
    "gaud malhar": "4L8L8L8L8L8",
    "bhairavi": "F0f-pYn-E-A",
    "bhatiyar": "6L8L8L8L8L8",
    "multani": "7L8L8L8L8L8",
    "bihag": "8L8L8L8L8L8",
    "hameer": "9L8L8L8L8L8",
    "jog": "0L8L8L8L8L8",
    "kalyan": "1L8L8L8L8L8",
    "malkauns": "8qW1B5l8V9U",
    "chandrakauns": "3L8L8L8L8L8",
    "lagan gandhar": "4L8L8L8L8L8",
    "todi": "5L8L8L8L8L8",
    "shree": "6L8L8L8L8L8",
    "lalit pancham": "7L8L8L8L8L8",
    "bibhas": "8L8L8L8L8L8",
    "puriya": "9L8L8L8L8L8",
    "sawani": "0L8L8L8L8L8",
    "kedar": "1L8L8L8L8L8",
    "dhani": "2L8L8L8L8L8",
    "ramdasi malhar": "3L8L8L8L8L8"
}'''
text = re.sub(old_links, new_links, text, flags=re.DOTALL)

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

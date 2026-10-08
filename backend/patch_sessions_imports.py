import re

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'r', encoding='utf-8') as f:
    text = f.read()

if 'from fastapi import File, UploadFile' not in text:
    text = text.replace('from fastapi import APIRouter', 'from fastapi import APIRouter, File, UploadFile, HTTPException')

with open(r'd:\NADABRAHMA\backend\app\routers\sessions.py', 'w', encoding='utf-8') as f:
    f.write(text)

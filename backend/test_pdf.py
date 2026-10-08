import sys
import asyncio
sys.path.append(r'd:\NADABRAHMA\backend')
from app.db import SessionLocal
from app.models import User
from app.routers.me import export_my_data_pdf

async def test():
    db = SessionLocal()
    user = db.query(User).filter(User.email == 'sarvesh1910@gmail.com').first()
    res = export_my_data_pdf(user=user, db=db)
    print("PDF bytes:", len(res.body))
    with open('test_output.pdf', 'wb') as f:
        f.write(res.body)

asyncio.run(test())

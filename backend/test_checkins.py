import sys
sys.path.append(r'd:\NADABRAHMA\backend')
from app.db import SessionLocal
from app.models import CheckIn
db = SessionLocal()
checkins = db.query(CheckIn).all()
print("Moods:", set([c.mood for c in checkins]))
print("Energies:", set([c.energy for c in checkins]))

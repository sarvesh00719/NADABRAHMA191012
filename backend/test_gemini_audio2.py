import os
os.chdir(r'd:\NADABRAHMA\backend')
import sys
sys.path.append(r'd:\NADABRAHMA\backend')
from app.config import settings
from google import genai
from google.genai import types

client = genai.Client(api_key=settings.gemini_api_key)
print("Gemini client initialized.")

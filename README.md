# Nadbrahma (नादब्रह्म)

A compassionate, self-reflection companion app designed with a "do-no-harm" architecture.

## Overview
- **Backend:** FastAPI, SQLite, SQLAlchemy. Implements secure JWT auth, rate limiting, strict safety logic, and a dynamic conversation Stage Picker (Listen -> Reflect -> Explore -> Wrap-up). Includes Gemini integration and the `Kangiten` in-house PyTorch model scaffolding.
- **Mobile:** React Native (Expo Router). Implements a calm UI for daily check-ins, chatting with the companion, reviewing session summaries, and self-guided activities (box breathing, grounding).

## Getting Started
### Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
pytest
uvicorn app.main:app --reload
```

### Mobile
```bash
cd mobile
npm install
npx expo start
```

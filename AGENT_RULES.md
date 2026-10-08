# AGENT RULES (place at repo root as AGENT_RULES.md)

You are building Nadbrahma, a self-reflection and wellbeing companion app. Read `docs/01_IMPLEMENTATION_PLAN.md`, `docs/03_CONTRACTS.md` and `docs/07_COUNSELOR_AND_SAFETY.md` before changing code. They are the source of truth. If a request conflicts with them, stop and say so.

## Hard rules
1. Identity comes only from the verified JWT. Never accept `user_id` in a body, query or path for ownership.
2. Every database query that touches user data is scoped to the current user. Other users' resources return 404.
3. API keys and secrets live only in `backend/.env`. Never in mobile code, never in git, never in logs.
4. Crisis detection runs in plain code before any engine call. The engine is never called for a crisis message.
5. Never log message text, passwords or tokens.
6. All engines implement `ConversationEngine`. The rest of the app never imports Gemini or Kangiten directly.
7. If an engine fails, use the fallback chain, then a template. Never return a raw exception to the user.
8. No diagnosis wording anywhere in code, prompts, templates or UI. The app does not claim to be therapy or medical care.
9. Handoff to the Raga site sends only the versioned payload in the contract, only after the session is `reviewed` and consent is true. Never send a transcript.
10. No raw audio, video or images are stored. Voice and camera are not part of the MVP.
11. All user-visible strings in the mobile app use i18n keys (en, hi, mr).
12. Follow the contracts exactly: field names, status codes, error codes.

## Code rules
- Backend: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, type hints on all functions.
- Mobile: Expo + Expo Router + TypeScript strict mode. Function components and hooks.
- Pin dependency versions after the first successful install. Do not invent package names or versions. If an install fails, report it.
- Small files, one responsibility each, following the structure in the plan.
- Every endpoint gets at least one pytest test (success and an authorization failure).
- Keep the UI simple: one primary action per screen, large touch targets, labels on every control.

## Working method
- Do one task at a time. Finish it, run it, show the result.
- After each task state: files changed, how to run it, how it was checked, and what is not done.
- Do not refactor unrelated files. Do not add features outside the current task.
- When something is unclear, ask one precise question instead of guessing.
- Do not create placeholder code that pretends to work. Mark unfinished parts with `TODO(step N)` and list them.

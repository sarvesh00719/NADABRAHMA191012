# ANTIGRAVITY PROMPTS (paste in order)

Before the first prompt: create the repo, put `AGENT_RULES.md` in the root and the other documents in `docs/`.
After every prompt: run it, read the diff, commit.

---

## P0: Setup
```
Read AGENT_RULES.md and docs/01_IMPLEMENTATION_PLAN.md.
Create the repository structure from section 4 of the plan (folders and empty files are fine except where stated).
Backend: create requirements.txt (fastapi, uvicorn[standard], sqlalchemy, pydantic, pydantic-settings, pyjwt, argon2-cffi, slowapi, google-genai, httpx, pytest, python-multipart, email-validator). Create .env.example exactly as in section 5.1. Create app/main.py with GET /api/v1/health, CORS from config, and a request-id middleware. Create app/config.py using pydantic-settings.
Mobile: create an Expo app with TypeScript and Expo Router in /mobile, with .env.example containing EXPO_PUBLIC_API_URL.
Add a .gitignore that excludes .env, *.db, node_modules, checkpoints.
Done when: `uvicorn app.main:app --reload --host 0.0.0.0` serves /api/v1/health and `npx expo start` opens on a phone.
```

## P1: Backend core (auth, profile)
```
Implement per docs/03_CONTRACTS.md sections Auth and Profile.
Files: app/db.py, app/models.py (users, preferences, audit_events for now), app/schemas.py, app/security.py, app/deps.py, app/errors.py, routers/auth.py, routers/me.py.
Use SQLAlchemy 2.0 with DATABASE_URL (SQLite default). Create tables at startup.
Passwords hashed with argon2. JWT with sub=user id and expiry from config. get_current_user in deps.py is the only identity source.
All errors use the standard error format with request_id.
Add rate limiting on login (10 per minute per IP).
Write tests/test_auth.py: register, duplicate email, login, wrong password, /me with and without token, expired token.
Done when: pytest passes and the flow works in /docs.
```

## P2: Check-ins, activities, feedback
```
Implement Check-ins, Activities and Feedback per docs/03_CONTRACTS.md.
Add tables check_ins, activity_events, feedback to models.py.
Activities come from app/content/activities.json (breathing 4-4-6 cycles, 5-4-3-2-1 grounding, wind-down sequence); use text_key values for i18n, no hard-coded user text.
trend_available is true when the user has 5 or more check-ins.
Write tests: create/list check-ins, ownership (user B cannot see user A's items), invalid values rejected.
Done when: pytest passes.
```

## P3: Sessions, chat, safety, stub engine
```
Implement Sessions per docs/03_CONTRACTS.md using the message flow in section 5.4 of the plan.
Add tables sessions, messages, session_reviews.
Create services/engines/base.py (interface from section 5.6), stub.py (fixed reply per stage), registry.py (reads ENGINE and ENGINE_FALLBACK).
Create services/safety.py with check_crisis (loads content/crisis_phrases.json, normalizes text: lowercase, strip punctuation, Unicode NFC, collapse spaces, matches phrases) and validate_output (rules from docs/07_COUNSELOR_AND_SAFETY.md).
Create services/stage.py per section 5.5.
Create content/crisis_phrases.json, crisis_resources.json, fallback_templates.json from docs/07_COUNSELOR_AND_SAFETY.md.
The crisis check runs before the engine. On a crisis match the engine is not called.
Idempotency: unique (session_id, client_message_id).
Rate limit messages to 30 per minute per user.
Write tests/test_sessions.py, test_ownership.py, test_safety.py: lifecycle, duplicate message id, other user's session returns 404, ended session rejects messages, crisis phrases in English/Hindi/Marathi/romanized never call the engine (use a mock engine that fails if called), invalid engine output triggers fallback.
Done when: pytest passes and a full stub chat works through /docs.
```

## P4: Mobile foundation
```
Read docs/01_IMPLEMENTATION_PLAN.md section 6 and docs/03_CONTRACTS.md.
Build in /mobile: theme (calm colors, large readable type), reusable Button/Input/Card with accessibilityLabel and accessibilityRole, src/api/client.ts (fetch wrapper using EXPO_PUBLIC_API_URL, adds Bearer token, parses the standard error format, clears token on 401), src/api/types.ts matching the contracts, src/auth/AuthContext.tsx using expo-secure-store, i18n setup (i18next, react-i18next, expo-localization) with en.json, hi.json, mr.json and all strings as keys.
Screens: welcome, register, login, onboarding needs, onboarding privacy (saves via PATCH /me), home, check-in, activities list with breathing, grounding, winddown (each with pause, skip, exit; send activity events).
Routing: unauthenticated -> welcome; authenticated and onboarding not done -> onboarding; else tabs (home, activities, history, profile).
Done when: on a physical phone I can register, finish onboarding, save a check-in and complete a breathing exercise.
```

## P5: Mobile chat
```
Build session/setup.tsx and session/[id].tsx.
Setup: language, goal, retention, Start (POST /sessions with a generated client_request_id).
Chat: message list with stable ids; user message appears immediately; assistant shows a pending indicator; failed sends show Retry reusing the same client_message_id; unsent text saved as a draft in AsyncStorage; pause and End buttons always visible; End calls POST /sessions/{id}/end and goes to the review screen.
If the response has crisis != null, show a clear crisis card with the resources and tap-to-call links. Do not auto-dial.
Support large system fonts and screen readers.
Done when: a real chat works on the phone against ENGINE=stub, a crisis phrase shows the card, airplane mode keeps the draft and retry works.
```

## P6: Gemini engine
```
Implement services/engines/gemini.py using the google-genai SDK.
System instruction = content of app/content/counselor_rules.md plus a one-line stage hint (for example: "Stage: reflect. Reflect back what the user said in one sentence, then ask one gentle question.").
Settings: temperature 0.6, max output tokens about 200, 10 second timeout, model name from GEMINI_MODEL, key from GEMINI_API_KEY.
Map EngineContext.history to the SDK message format. Respond in ctx.language.
On any exception raise EngineUnavailable so the registry fallback chain handles it.
Do not log prompts or replies.
Write a test using a mocked client for the success path and the failure path.
Done when: ENGINE=gemini gives counselor-style replies, and a wrong key falls back to the stub reply without crashing.
```

## P7: Summary, review, history (backend)
```
Implement POST /sessions/{id}/end, POST /sessions/{id}/review and GET /history per docs/03_CONTRACTS.md using services/summary.py (template and extractive only, section 5.8; no model call).
Review is allowed only when status is ended. Approval sets status reviewed and stores final_summary, topics, reflection.
If the session retention is delete_on_end, delete its messages on approval.
Tests: draft contents, edit and approve, cannot review an active session, cannot review another user's session, retention deletion works.
Done when: pytest passes.
```

## P8: Mobile review and history
```
Build session/review/[id].tsx: editable draft summary, topic chips (from suggested_topics plus add custom), reflection field, Approve button, then optional feedback (helpful, neutral, not helpful) and a button "Explore music recommendation" that opens raga/[id].
Build (tabs)/history.tsx listing reviewed sessions and check-ins with a simple detail view. Show the trend only when trend_available is true, labeled "Your own self-reported check-ins".
Done when: end session, edit, approve and see it in history on the phone.
```

## P9: Raga handoff
```
Before coding: I will tell you what inputs my Raga site takes and whether it has an API. Ask me if I have not.
Implement services/raga/mapping.py (the only file that knows the Raga site's input names), services/raga/adapter.py (RAGA_MODE=api posts the mapped payload to RAGA_API_URL with RAGA_API_KEY and a 10 second timeout; RAGA_MODE=link builds a URL on RAGA_SITE_URL with query params), routers/raga.py with the preview GET and consent POST from docs/03_CONTRACTS.md, and table raga_handoffs.
Rules: only for status reviewed; consent must be true; payload exactly as in the contract; store it; never send messages.
Mobile raga/[id].tsx: show the exact payload from the preview in plain language, a consent checkbox, Send; then show the result list or open the link with expo-web-browser.
Tests with a fake HTTP server: blocked before review, blocked without consent, payload matches preview, upstream failure returns ENGINE_UNAVAILABLE.
Done when: the handoff reaches my real Raga site and returns to the app.
```

## P10: Kangiten
Use `docs/06_KANGITEN_V0.md`. Give the agent the "Build tasks" list there, one task at a time.
Then implement `services/engines/kangiten.py`:
```
Implement KangitenEngine per section 5.6 and docs/06_KANGITEN_V0.md section 8. Load the SentencePiece tokenizer and checkpoint once at startup. Build the prompt in the format at the end of docs/03_CONTRACTS.md. Sample with temperature 0.7, top-k 40, max 80 new tokens, stop at <|end|>. Run on CPU unless CUDA is available. If the files are missing, raise EngineUnavailable. Add a test that loads a tiny random checkpoint and returns text.
Done when: ENGINE=kangiten answers in the app, and failure falls back.
```

## P11: Finish
```
1. Implement DELETE /me/data per section 5.11 with a test that no rows remain for that user.
2. Profile screen: language switch, retention switch, delete my data with confirmation, log out.
3. Fill hi.json and mr.json for every key in en.json. Mark any machine-translated string with a TODO for human review.
4. Accessibility pass on Home, Chat, Review: labels, roles, 44px targets, large-text layout.
5. Write README.md: what the app is, how to run backend and mobile, env variables, engine switch, what is Gemini, what is Kangiten, test commands, and the roadmap from docs/02_WORKFLOW_PLAN.md section 8.
6. Run the full pytest suite and fix failures.
Done when: the manual journey in docs/02_WORKFLOW_PLAN.md section 5 passes on a phone.
```

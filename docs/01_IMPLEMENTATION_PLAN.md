# NADBRAHMA: IMPLEMENTATION PLAN (v2, final for MVP)

A mobile self-reflection and wellbeing companion. It is not a medical or therapy tool and must never say it is.

---

## 1. Scope

### In the MVP
1. Register, login, profile (own backend, JWT)
2. Onboarding (needs, language, interaction preference) and Privacy Center
3. Self-reported check-in (mood, energy, need, optional note)
4. Activities: breathing, grounding, bedtime wind-down
5. Text chat with counselor rules and a hard-coded crisis router
6. Conversation engines behind one interface: Stub, Gemini, Kangiten v0
7. End session, draft summary, user edit, approve
8. History of sessions and check-ins
9. Feedback on sessions
10. Raga handoff to the existing ML website (consent-gated, minimum data)
11. Delete my data
12. UI languages: English, Hindi, Marathi (strings only)

### Stretch (only if time remains)
Reminders (local notifications), trend chart (after 5 or more check-ins), PDF export.

### Not in the MVP (roadmap)
Voice, camera/facial observation, provider sharing, on-device model, Redis, GPU hosting, Alembic migrations.

---

## 2. Architecture

```
MOBILE (Expo + React Native + TypeScript)
  Screens -> API client -> secure token storage
        |  HTTPS + Bearer JWT
        v
BACKEND (FastAPI)
  auth -> ownership check -> session controller
        |
        v
  input validation -> CRISIS ROUTER (rules) -> stage picker
        |
        v
  ConversationEngine interface
     |- StubEngine      (fixed replies, for tests)
     |- GeminiEngine    (API key on server only)
     |- KangitenEngine  (own model, loaded in the backend)
        |
        v
  output validator -> fallback template if invalid
        |
        v
  DATABASE (SQLite in dev, PostgreSQL in prod)
        |
        v
  user review -> approved summary -> RAGA ADAPTER -> existing Raga website/API
```

Rules that never change:
- The mobile app contains no model logic and no API keys.
- Crisis detection runs in plain code before any model sees the text.
- The engine is chosen by an environment variable. The rest of the app does not know which engine answered.
- Raw media is not part of the MVP, so none is stored.

---

## 3. Tech stack

| Layer | Choice | Reason |
|---|---|---|
| Mobile | Expo (current stable SDK), Expo Router, TypeScript | One codebase, runs on a phone through Expo Go |
| Mobile data | TanStack Query | Simple fetching, retry, caching |
| Mobile storage | expo-secure-store (token), AsyncStorage (unsent drafts) | Token stays protected |
| i18n | i18next, react-i18next, expo-localization | en, hi, mr |
| Backend | Python 3.11+, FastAPI, Uvicorn | Typed, auto docs at /docs |
| Validation | Pydantic v2 | Request/response contracts |
| ORM | SQLAlchemy 2.0 | SQLite now, Postgres by changing one URL |
| Passwords | argon2-cffi (or bcrypt) | Never store plaintext |
| Tokens | PyJWT, HS256, secret from env | Simple and sufficient for MVP |
| Rate limit | slowapi | Login and chat endpoints |
| LLM | google-genai SDK, model name from env | Prototype engine |
| Own model | PyTorch, SentencePiece | Kangiten v0 |
| Tests | pytest + httpx | Authorization and safety tests |
| Hosting (demo) | Local uvicorn + phone on same Wi-Fi, or a tunnel (cloudflared / ngrok) | Fastest for 2 days |
| Hosting (later) | One container + managed Postgres | |

Auth decision: the earlier plan used Firebase. For a 2-day build, own email/password + JWT is faster, has no external setup, and keeps login, profile and database fully working in your own backend. Firebase can replace it later behind the same `get_current_user` function.

Known limits of this choice: one access token (7 days), no email verification, no password reset by email. List these in the README as roadmap items.

---

## 4. Repository structure

```
nadbrahma/
  README.md
  AGENT_RULES.md
  docs/
    01_IMPLEMENTATION_PLAN.md
    02_WORKFLOW_PLAN.md
    03_CONTRACTS.md
    05_ANTIGRAVITY_PROMPTS.md
    06_KANGITEN_V0.md
    07_COUNSELOR_AND_SAFETY.md
  backend/
    requirements.txt
    .env.example
    app/
      main.py
      config.py
      db.py
      models.py
      schemas.py
      deps.py                  # get_db, get_current_user
      errors.py
      security.py              # hash, verify, create/decode token
      routers/
        auth.py
        me.py
        checkins.py
        sessions.py
        activities.py
        feedback.py
        raga.py
        health.py
      services/
        session_service.py     # message flow, end, review
        summary.py             # extractive draft summary
        safety.py              # crisis router + output validator
        stage.py               # conversation stage picker
        engines/
          base.py              # ConversationEngine interface
          stub.py
          gemini.py
          kangiten.py
          registry.py
        raga/
          adapter.py
          mapping.py
      content/
        counselor_rules.md
        crisis_phrases.json
        crisis_resources.json
        fallback_templates.json
        activities.json
    tests/
      test_auth.py
      test_ownership.py
      test_checkins.py
      test_sessions.py
      test_safety.py
      test_raga.py
  mobile/
    package.json
    app.json
    .env.example
    app/
      _layout.tsx
      index.tsx
      (auth)/welcome.tsx
      (auth)/login.tsx
      (auth)/register.tsx
      (onboarding)/needs.tsx
      (onboarding)/privacy.tsx
      (tabs)/_layout.tsx
      (tabs)/home.tsx
      (tabs)/activities.tsx
      (tabs)/history.tsx
      (tabs)/profile.tsx
      check-in.tsx
      session/setup.tsx
      session/[id].tsx
      session/review/[id].tsx
      raga/[id].tsx
      activity/breathing.tsx
      activity/grounding.tsx
      activity/winddown.tsx
    src/
      api/client.ts
      api/types.ts
      auth/AuthContext.tsx
      components/
      theme/
      localization/{en,hi,mr}.json
      storage/drafts.ts
  kangiten/
    data/
    tokenizer/
    model/
    training/
    inference/
    evaluation/
```

---

## 5. Backend design

### 5.1 Environment variables (`backend/.env.example`)
```
APP_ENV=dev
DATABASE_URL=sqlite:///./nadbrahma.db
JWT_SECRET=change-me-long-random
JWT_EXPIRE_MINUTES=10080
ENGINE=gemini                # stub | gemini | kangiten
ENGINE_FALLBACK=stub
GEMINI_API_KEY=
GEMINI_MODEL=                # set to a current model name from Google AI Studio
KANGITEN_CHECKPOINT=../kangiten/checkpoints/latest.pt
KANGITEN_TOKENIZER=../kangiten/tokenizer/tok.model
RAGA_MODE=link               # api | link
RAGA_API_URL=
RAGA_API_KEY=
RAGA_SITE_URL=
CORS_ORIGINS=*
```
`.env` is git-ignored. Keys never go in the mobile app.

### 5.2 Database tables (MVP)

| Table | Columns |
|---|---|
| users | id, email (unique), password_hash, display_name, locale, status, created_at |
| preferences | user_id (PK/FK), language, interaction_mode, needs (JSON list), retention (`keep` or `delete_on_end`), onboarding_done |
| check_ins | id, user_id, created_at, mood, energy, need, note |
| sessions | id, user_id, status (`active`, `ended`, `reviewed`), language, goal, started_at, ended_at, retention, crisis_flag |
| messages | id, session_id, client_message_id, role (`user`/`assistant`), content, created_at, engine, model_version, safety_route |
| session_reviews | id, session_id, draft_summary, final_summary, topics (JSON), reflection, reviewed_at |
| activity_events | id, user_id, session_id (nullable), activity_key, action (`start`, `complete`, `skip`), created_at |
| feedback | id, user_id, session_id, choice, comment, created_at |
| raga_handoffs | id, session_id, user_id, payload (JSON), mode, status, created_at |
| audit_events | id, user_id, event_type, target, created_at |

Constraints:
- Unique (session_id, client_message_id) for idempotent retries.
- Every table that holds user data has `user_id` or reaches it through `sessions.user_id`.
- Activities are static content in `activities.json`, not a table.
- No raw audio, video or frames anywhere.

### 5.3 Auth and ownership
- Register: validate email, minimum password length 8, hash, create user and empty preferences.
- Login: verify hash, return JWT containing `sub` = user id, `exp`.
- `get_current_user` decodes the token and loads the user. It is the only source of identity.
- Never accept `user_id` in a request body or query.
- Every query filters by the current user. A resource owned by someone else returns 404, not 403.
- Rate limits: login 10 per minute per IP, messages 30 per minute per user.
- Audit events: register, login failure threshold, data deletion, raga handoff, crisis route (event only, no message content).

### 5.4 Message flow (`session_service.send_message`)
1. Load session, confirm ownership and `status == active`.
2. Idempotency: if `client_message_id` exists, return the stored pair.
3. Validate text: trim, 1 to 1000 characters.
4. Save the user message.
5. `safety.check_crisis(text)`:
   - match: save assistant message with `safety_route=crisis`, set `sessions.crisis_flag`, write audit event, return the crisis payload. **The engine is not called.**
6. `stage.pick(session, history)` returns one of `listen`, `reflect`, `explore`, `suggest_activity`, `wrap_up`.
7. Build `EngineContext`: language, stage, goal, latest check-in (mood, energy, need), last 8 messages.
8. `engine.reply(ctx)` with a 10 second timeout.
9. `safety.validate_output(text)`. If invalid, retry once. If still invalid or the engine fails, use the next engine in the fallback chain, then a template from `fallback_templates.json`.
10. Save the assistant message with engine name, model_version, safety_route.
11. Return both messages.

### 5.5 Stage rules (`stage.py`)
- Turn 1: `listen`
- If the last user message is under 6 words: `explore`
- Alternate `reflect` and `explore` otherwise
- If check-in energy is low or mood is `stressed`/`restless` and no activity was suggested in this session: `suggest_activity`
- Turn 8 or later, or user says goodbye: `wrap_up`

### 5.6 Engine interface (`engines/base.py`)
```python
class EngineContext(BaseModel):
    language: str
    stage: str
    goal: str | None
    checkin: dict | None
    history: list[dict]          # [{"role": "user"|"assistant", "content": str}]

class EngineReply(BaseModel):
    text: str
    engine: str
    model_version: str

class ConversationEngine(Protocol):
    name: str
    version: str
    async def reply(self, ctx: EngineContext) -> EngineReply: ...
```
`registry.get_engine()` reads `ENGINE`, returns the chain `[primary, fallback]`.

- **StubEngine:** returns a fixed reply per stage. Used in tests and for building the app before keys exist.
- **GeminiEngine:** system instruction = `counselor_rules.md` + the stage hint. Temperature about 0.6, max output about 200 tokens. Maps `history` to the SDK format.
- **KangitenEngine:** formats the prompt with the special tokens, samples with max 80 new tokens, strips at the end token. Loaded once at startup. If the checkpoint is missing, it raises, and the fallback chain takes over.

### 5.7 Output validator rules (`safety.validate_output`)
Reject if any applies: empty, longer than 600 characters, more than 4 sentences, identical to the previous assistant message, contains a forbidden pattern (diagnosis wording, medication advice, claims to be a therapist or doctor, guarantees), contains a URL or phone number not in `crisis_resources.json`. Full list in `07_COUNSELOR_AND_SAFETY.md`.

### 5.8 Summary (`summary.py`)
No model needed. Draft summary is built from a template:
- Date, duration, language, mode
- Check-in at start (self-reported)
- Activities completed
- User statements: the user's own messages, trimmed, up to 5
- Topics: user selects from chips at review, stored in `session_reviews.topics`
- Reflection / next step: empty, for the user to write

The user edits and approves. `final_summary` is saved only on approval. Only `final_summary` appears in history and export.

If `retention=delete_on_end`, messages are deleted when the review is approved, and only the final summary stays.

### 5.9 Raga handoff
The existing Raga website stays separate. The backend has one adapter.

Preview: `GET /raga/handoff/{session_id}` returns the exact payload that would be sent. The user sees it.

Send: `POST /raga/handoff/{session_id}` with `{"consent": true}`:
- Only allowed if the session is `reviewed` and consent is true.
- Payload (versioned):
```json
{
  "handoff_version": "1",
  "session_id": "S123",
  "language": "en",
  "user_goal": "reflection",
  "user_reported_topics": ["exam pressure"],
  "mood": "stressed",
  "energy": "low",
  "need": "calm",
  "session_duration_sec": 620,
  "feedback": "helpful"
}
```
- `RAGA_MODE=api`: POST the payload (mapped by `raga/mapping.py`) to `RAGA_API_URL` with `RAGA_API_KEY`, return the result.
- `RAGA_MODE=link`: build a URL to `RAGA_SITE_URL` with query parameters from the mapping, return `{"url": "..."}`. The app opens it in the browser.
- Store the payload in `raga_handoffs`. Never send transcripts.

`mapping.py` is the only file that knows the Raga site's input format. Before building this step, open your Raga site and note what inputs it takes (mood, time of day, goal, and so on), then edit the mapping table in that file.

### 5.10 Errors
All errors use:
```json
{"error": {"code": "SESSION_NOT_FOUND", "message": "Session is unavailable.", "request_id": "..."}}
```
Codes: `VALIDATION_ERROR`, `UNAUTHORIZED`, `INVALID_CREDENTIALS`, `EMAIL_TAKEN`, `SESSION_NOT_FOUND`, `SESSION_NOT_ACTIVE`, `RATE_LIMITED`, `ENGINE_UNAVAILABLE`, `CONSENT_REQUIRED`, `NOT_REVIEWED`, `INTERNAL`.

### 5.11 Delete my data
`DELETE /me/data`: delete messages, reviews, check-ins, activity events, feedback, handoffs, preferences, sessions, then the user. Write an audit event first with only the user id and timestamp. Return 204.

---

## 6. Mobile design

### 6.1 Screens
| Screen | Behavior |
|---|---|
| Welcome | App name, Get Started, I have an account |
| Register / Login | Email, password, clear error messages |
| Onboarding: needs | Choose needs (calm, sleep, focus, reflect), language, interaction preference |
| Onboarding: privacy | Plain-language explanation, retention choice, saved to preferences |
| Home | Check-in card, Start session, quick activities, recent items |
| Check-in | Mood (Great, Good, Okay, Low, Stressed, Tired, Restless), energy, need, optional note |
| Session setup | Language, goal, retention, Start |
| Chat | Message list, input, pause and End buttons always visible, crisis card when triggered |
| Review | Draft summary editable, topic chips, reflection, Approve |
| Raga consent | Shows the exact payload, checkbox, Send, then opens the result |
| History | Reviewed sessions and check-ins |
| Activities | Breathing, grounding, wind-down, each with pause, skip, exit |
| Profile | Language, retention, delete my data, log out |

### 6.2 Behavior rules
- Token in secure store. On 401, clear it and go to Login.
- Chat: user message appears immediately. Assistant shows a pending state. Failed messages show Retry and reuse the same `client_message_id`.
- Unsent text is saved as a draft locally.
- Every screen works with larger system text. Buttons at least 44 px. Every control has `accessibilityLabel` and `accessibilityRole`. No meaning conveyed by color alone.
- No hard-coded strings. All text via i18n keys.
- Crisis card: shows the resources returned by the backend, with tap-to-call. It does not auto-dial.
- API base URL from `EXPO_PUBLIC_API_URL`. On a physical phone, use the computer's LAN IP or a tunnel URL, not `localhost`.

---

## 7. Kangiten v0
See `06_KANGITEN_V0.md`. It runs as `KangitenEngine` behind the same interface. It becomes the primary engine only if it passes the gates in that file. Until then the primary is Gemini, and the presentation must say so.

---

## 8. Security and privacy checklist
- HTTPS for any non-local deployment.
- Passwords hashed. JWT secret from env.
- Ownership enforced on every query. Tests prove cross-user access fails.
- Logs never contain message text, passwords or tokens.
- API keys only in backend env.
- CORS limited outside dev.
- Gemini free tier may use inputs to improve products. Use test data only until a paid or privacy-appropriate plan is in place.
- Privacy Center in the app explains what is stored, lets the user choose retention, and deletes everything.
- Age: state "18 and above" in onboarding and terms until a minors policy জৈন policy exists.
- Compliance work outside code (before real users): privacy policy and terms, consent text reviewed against India's DPDP Act 2023, a clinical or counseling advisor reviewing the safety content.

---

## 9. Definition of done (MVP)
1. Fresh install on a phone: register, onboard, check-in, chat, review, history all work.
2. Two accounts cannot see each other's data (automated test passes).
3. Crisis phrases in English, Hindi, Marathi and romanized forms show the safety card and never reach an engine (automated test passes).
4. With `ENGINE=stub`, `gemini`, and `kangiten`, the same chat flow works. If an engine fails, the fallback answers.
5. Raga handoff sends only the approved payload and returns a result or link.
6. Delete my data removes everything for that user.
7. README states what is Gemini, what is Kangiten, and what is roadmap.

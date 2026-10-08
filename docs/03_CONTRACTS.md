# NADBRAHMA: API CONTRACTS

Base path: `/api/v1`. JSON only. Auth: `Authorization: Bearer <token>` on everything except register, login and health.
Timestamps are ISO 8601 UTC. IDs are strings.

Error format (all errors):
```json
{"error": {"code": "SESSION_NOT_FOUND", "message": "Session is unavailable.", "request_id": "abc123"}}
```

---

## Health
`GET /health` -> `200 {"status": "ok", "engine": "gemini", "version": "1"}`

## Auth

`POST /auth/register`
```json
{"email": "a@b.com", "password": "min8chars", "display_name": "Asha"}
```
-> `201`
```json
{"access_token": "...", "token_type": "bearer", "user": {"id": "u1", "email": "a@b.com", "display_name": "Asha", "locale": "en"}}
```
Errors: `EMAIL_TAKEN` (409), `VALIDATION_ERROR` (422)

`POST /auth/login`
```json
{"email": "a@b.com", "password": "..."}
```
-> `200` same body as register. Error: `INVALID_CREDENTIALS` (401)

## Profile

`GET /me` -> `200`
```json
{
  "id": "u1", "email": "a@b.com", "display_name": "Asha", "locale": "en",
  "preferences": {"language": "en", "interaction_mode": "text", "needs": ["calm"], "retention": "keep", "onboarding_done": true}
}
```

`PATCH /me` (any subset)
```json
{"display_name": "Asha", "preferences": {"language": "hi", "needs": ["calm", "sleep"], "retention": "delete_on_end", "onboarding_done": true}}
```
-> `200` same shape as GET.

`DELETE /me/data` -> `204`

## Check-ins

Allowed values: mood `great|good|okay|low|stressed|tired|restless`, energy `low|medium|high`, need `calm|sleep|focus|reflect|connect`.

`POST /check-ins`
```json
{"mood": "stressed", "energy": "low", "need": "calm", "note": "exam tomorrow"}
```
-> `201` `{"id": "c1", "created_at": "...", "mood": "...", "energy": "...", "need": "...", "note": "..."}`

`GET /check-ins?limit=30` -> `200` `{"items": [ ... ], "trend_available": false}`
`trend_available` is true when the user has 5 or more check-ins.

## Activities

`GET /activities` -> `200`
```json
{"items": [{"key": "breathing", "title_key": "activity.breathing", "duration_sec": 180, "steps": [{"text_key": "...", "seconds": 4}]}]}
```
Keys: `breathing`, `grounding`, `winddown`.

`POST /activities/events`
```json
{"activity_key": "breathing", "action": "complete", "session_id": null}
```
`action`: `start|complete|skip`. -> `201`

## Sessions

`POST /sessions`
```json
{"language": "en", "goal": "reflection", "retention": "keep", "client_request_id": "R1"}
```
`goal`: `reflection|grounding|clarity|just_talk`. `client_request_id` makes creation idempotent.
-> `201`
```json
{"id": "S123", "status": "active", "language": "en", "goal": "reflection", "started_at": "...", "opening_message": {"id": "m0", "role": "assistant", "content": "..."}}
```

`POST /sessions/{id}/messages`
```json
{"client_message_id": "M456", "text": "I feel stressed about exams."}
```
-> `200`
```json
{
  "user_message": {"id": "m1", "role": "user", "content": "...", "created_at": "..."},
  "assistant_message": {
    "id": "m2", "role": "assistant", "content": "What feels hardest right now?",
    "engine": "gemini", "model_version": "...", "safety_route": "normal", "created_at": "..."
  },
  "crisis": null
}
```
`safety_route`: `normal|clarify|fallback|crisis`.

Crisis response (engine not called):
```json
{
  "user_message": {...},
  "assistant_message": {"id": "m2", "role": "assistant", "content": "I'm really glad you told me. You deserve support from a person right now.", "engine": "rules", "model_version": "1", "safety_route": "crisis", "created_at": "..."},
  "crisis": {"message": "...", "resources": [{"name": "...", "contact": "...", "type": "phone"}]}
}
```
Errors: `SESSION_NOT_FOUND` (404), `SESSION_NOT_ACTIVE` (409), `VALIDATION_ERROR` (422), `RATE_LIMITED` (429).
Repeating the same `client_message_id` returns the original response, no duplicates.

`GET /sessions/{id}` -> `200` session fields + `messages` list (empty if retention deleted them).

`POST /sessions/{id}/end` -> `200`
```json
{
  "id": "S123", "status": "ended", "duration_sec": 620,
  "draft": {
    "summary": "Session on 04 Oct, 10 min, English.\nStarted feeling: stressed, energy low, need: calm.\nActivities: breathing.\nYou said:\n- ...",
    "suggested_topics": ["exam pressure", "overthinking"]
  }
}
```

`POST /sessions/{id}/review`
```json
{"final_summary": "edited text", "topics": ["exam pressure"], "reflection": "Take a walk tomorrow.", "approve": true}
```
-> `200` `{"id": "S123", "status": "reviewed", "reviewed_at": "..."}`
If retention is `delete_on_end`, messages are deleted here.
Only allowed when status is `ended`.

`GET /history?limit=20` -> `200`
```json
{"items": [{"type": "session", "id": "S123", "date": "...", "final_summary": "...", "topics": ["..."], "duration_sec": 620}, {"type": "check_in", "id": "c1", "date": "...", "mood": "low"}]}
```

## Feedback
`POST /feedback`
```json
{"session_id": "S123", "choice": "helpful", "comment": ""}
```
`choice`: `helpful|neutral|not_helpful`. -> `201`

## Raga handoff

`GET /raga/handoff/{session_id}` -> `200` (preview, nothing is sent)
```json
{
  "handoff_version": "1",
  "session_id": "S123", "language": "en", "user_goal": "reflection",
  "user_reported_topics": ["exam pressure"], "mood": "stressed", "energy": "low", "need": "calm",
  "session_duration_sec": 620, "feedback": "helpful"
}
```
Error: `NOT_REVIEWED` (409) unless session status is `reviewed`.

`POST /raga/handoff/{session_id}`
```json
{"consent": true}
```
-> `200`
```json
{"mode": "link", "url": "https://raga-site.example/?mood=stressed&need=calm", "result": null}
```
or in api mode
```json
{"mode": "api", "url": null, "result": {"ragas": [{"name": "...", "reason": "...", "listen_url": "..."}]}}
```
Errors: `CONSENT_REQUIRED` (400), `NOT_REVIEWED` (409), `ENGINE_UNAVAILABLE` (502, when the Raga service is down).

## Engine interface (internal, Python)
```python
EngineContext = {"language": "en", "stage": "listen|reflect|explore|suggest_activity|wrap_up", "goal": "...", "checkin": {"mood": "...", "energy": "...", "need": "..."} | None, "history": [{"role": "user", "content": "..."}]}
EngineReply   = {"text": "...", "engine": "gemini", "model_version": "..."}
```

## Kangiten prompt format (internal)
```
<|bos|><|stage:listen|><|lang:en|>
<|user|> I feel stressed about exams. <|end|>
<|assistant|> What feels hardest right now? <|end|>
```

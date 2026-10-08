def map_payload_to_raga_query(payload: dict) -> dict:
    return {
        "mood": payload.get("mood", "unknown"),
        "need": payload.get("need", "unknown"),
        "goal": payload.get("user_goal", "unknown"),
        "lang": payload.get("language", "en")
    }

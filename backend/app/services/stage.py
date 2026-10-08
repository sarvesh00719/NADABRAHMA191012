def pick(session, history: list) -> str:
    if len(history) == 0:
        return "listen"
        
    if len(history) >= 14:
        return "wrap_up"
        
    last_user_msg = history[-1]["content"] if history and history[-1]["role"] == "user" else ""
    
    if "goodbye" in last_user_msg.lower() or "bye" in last_user_msg.lower():
        return "wrap_up"
        
    if len(last_user_msg.split()) < 6:
        return "explore"
        
    assistant_count = sum(1 for m in history if m["role"] == "assistant")
    if assistant_count % 2 == 0:
        return "reflect"
    return "explore"

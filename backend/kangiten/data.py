import json
import os
from pathlib import Path

def prepare_data(db_sessions, output_file: str):
    """
    Format chat logs into JSONL for training.
    Expected format per line:
    {"text": "User: hello\\nAssistant: hi there\\n..."}
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for session in db_sessions:
            text = ""
            for msg in session.get("messages", []):
                role = "User" if msg["role"] == "user" else "Assistant"
                text += f"{role}: {msg['content']}\\n"
            
            f.write(json.dumps({"text": text.strip()}) + "\\n")
            
class DummyTokenizer:
    def __init__(self, vocab_size=50000):
        self.vocab_size = vocab_size
        self.pad_token_id = 0
        self.eos_token_id = 1
        
    def encode(self, text: str):
        # Dummy encoding: just use char ordinals
        return [ord(c) % self.vocab_size for c in text]
        
    def decode(self, tokens: list):
        return "".join([chr(t) if t > 31 else " " for t in tokens])

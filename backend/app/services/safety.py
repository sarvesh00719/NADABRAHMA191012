import json
import unicodedata
import re
from pathlib import Path
from typing import Optional, Dict

CONTENT_DIR = Path(__file__).parent.parent / "content"

def load_json(filename: str) -> dict:
    path = CONTENT_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

crisis_phrases = load_json("crisis_phrases.json")
crisis_resources = load_json("crisis_resources.json")
fallback_templates = load_json("fallback_templates.json")

def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def check_crisis(text: str) -> Optional[Dict]:
    norm_text = normalize_text(text)
    
    for lang, phrases in crisis_phrases.items():
        for phrase in phrases:
            norm_phrase = normalize_text(phrase)
            if norm_phrase in norm_text:
                return {
                    "message": "I'm really glad you told me. What you're feeling matters, and you deserve support from a real person right now. Please reach out to someone you trust, or use one of the helplines below.",
                    "resources": crisis_resources.get("resources", [])
                }
    return None

def validate_output(text: str, previous_assistant_message: str = None) -> bool:
    text = text.strip()
    if not text:
        return False
    if len(text) > 600:
        return False
        
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    if len(sentences) > 4:
        return False
        
    if previous_assistant_message and text.lower() == previous_assistant_message.strip().lower():
        return False
        
    forbidden_patterns = [
        "you have depression", "you are depressed", "you suffer from", 
        "diagnos", "disorder", "bipolar", "schizophren", "ptsd",
        "medication", "medicine", "dosage", "mg", "prescri", "antidepressant", "therapy will",
        "i am a therapist", "i am a doctor", "as your therapist", "as a counselor",
        "i promise", "guaranteed", "everything will be fine", "will definitely",
        "i feel your pain", "i am human", "i have a family"
    ]
    
    norm_out = text.lower()
    for pattern in forbidden_patterns:
        if pattern in norm_out:
            return False
            
    if "http" in norm_out or "www" in norm_out:
        return False
        
    return True

import re
with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new parse_symptoms_nlp function
new_func = '''
import os
import json
import google.genai as genai
from pydantic import BaseModel, Field

class Emotion(BaseModel):
    label: str = Field(description="anxiety, depression, grief, stress, insomnia, anger, fatigue, or pain")
    intensity: int = Field(description="Intensity from 1 to 10")
    timeframe: str = Field(description="e.g. today, past, chronic")
    confidence: float = Field(description="Confidence from 0.0 to 1.0")
    evidence: str = Field(description="Quote or reasoning from text")

class ClinicalProfile(BaseModel):
    current_emotions: list[Emotion]
    session_goal: str
    relevant_history: list[str]
    time_of_day: str = Field(description="morning, afternoon, evening, night, midnight, sunset, dawn")

def parse_symptoms_nlp(text: str) -> dict:
    \"\"\"
    Advanced Contextual NLP parser using Gemini LLM.
    Replaces the naive keyword bag-of-words approach.
    \"\"\"
    if not text.strip():
        # Fallback if empty
        return {
            "conditions": [], "phq2": 0, "gad2": 0, "pain": 0, "energy": 5, "time_of_day": "evening",
            "norm_scores": {k: 0 for k in SYMPTOM_KEYWORDS}, "confidence": 0,
            "nlp_summary": "Please describe how you feel in more detail.", "detected_symptoms": []
        }
        
    try:
        # We assume GEMINI_API_KEY is in the environment
        client = genai.Client()
        
        prompt = f"""
        Analyze the following counseling session summary or patient description.
        Extract the current emotions, session goal, and relevant history.
        Ignore old emotions that are no longer present.
        
        Text:
        {text}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': ClinicalProfile,
                'temperature': 0.1
            }
        )
        
        data = json.loads(response.text)
        
        # Build the norm_scores map
        norm = {k: 0 for k in SYMPTOM_KEYWORDS}
        active = []
        confidences = []
        
        for em in data.get("current_emotions", []):
            label = em["label"].lower()
            if label in norm:
                norm[label] = max(norm[label], em["intensity"])
                if em["timeframe"].lower() in ["today", "now", "current"]:
                    active.append(label)
                confidences.append(em["confidence"])
                
        # Fallback mappings for ML Recommender
        phq2_raw = (norm.get("depression", 0) + norm.get("grief", 0) * 0.5) / 10 * 6
        phq2     = min(6, round(phq2_raw))
        
        gad2_raw = (norm.get("anxiety", 0) + norm.get("stress", 0) * 0.5) / 10 * 6
        gad2     = min(6, round(gad2_raw))
        
        pain     = round(norm.get("pain", 0))
        energy   = max(0, round(10 - norm.get("fatigue", 0) * 0.8 - norm.get("depression", 0) * 0.2))
        
        time_detected = data.get("time_of_day", "evening").lower()
        if time_detected not in TIME_KEYWORDS:
            time_detected = "evening"
            
        avg_conf = int((sum(confidences) / len(confidences)) * 100) if confidences else 85
        
        cond_str = ", ".join(active[:3]).title() if active else "None detected"
        goal_str = data.get('session_goal', 'General wellbeing')
        
        nlp_summary = (
            f"?? **Contextual AI Analysis**\n"
            f"?? Detected: **{cond_str}**\n"
            f"?? Goal: {goal_str}\n"
            f"?? PHQ-2: {phq2}/6  |  GAD-2: {gad2}/6  |  ? Energy: {energy}/10\n"
            f"?? Context: {time_detected.capitalize()}  |  ? Confidence: {avg_conf}%"
        )
        
        return {
            "conditions":          active,
            "phq2":                phq2,
            "gad2":                gad2,
            "pain":                pain,
            "energy":              energy,
            "time_of_day":         time_detected,
            "norm_scores":         norm,
            "confidence":          avg_conf,
            "nlp_summary":         nlp_summary,
            "detected_symptoms":   active,
        }
    except Exception as e:
        print(f"LLM Parse Error: {e}")
        # Fallback to empty if LLM fails (e.g. no internet, rate limit)
        return {
            "conditions": [], "phq2": 0, "gad2": 0, "pain": 0, "energy": 5, "time_of_day": "evening",
            "norm_scores": {k: 0 for k in SYMPTOM_KEYWORDS}, "confidence": 0,
            "nlp_summary": f"Fallback mode active. LLM Error: {e}", "detected_symptoms": []
        }
'''

# Use regex to replace the old parse_symptoms_nlp function
# It starts at "def parse_symptoms_nlp(text: str) -> dict:"
# and ends right before "# 3.  CHART GENERATORS"
pattern = re.compile(r'def parse_symptoms_nlp\(text: str\) -> dict:.*?# 3\.  CHART GENERATORS', re.DOTALL)
new_content = pattern.sub(new_func + '\n# 3.  CHART GENERATORS', content)

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

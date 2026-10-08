with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pattern = r'f"[^"]*Contextual AI Analysis[^"]*".*?f"[^"]*Confidence[^"]*%"'
good_str = '''f"\\n?? **Contextual AI Analysis**\\n"
            f"?? Detected: **{cond_str}**\\n"
            f"?? Goal: {goal_str}\\n"
            f"?? PHQ-2: {phq2}/6  |  GAD-2: {gad2}/6  |  ? Energy: {energy}/10\\n"
            f"?? Context: {time_detected.capitalize()}  |  ? Confidence: {avg_conf}%"'''
text = re.sub(pattern, good_str, text, flags=re.DOTALL)

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

import re

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '''    prescription_md = f\"\"\"
## \U0001f3b5 Your Personalised Raga Prescription

{parsed['nlp_summary']}

---
\"\"\"
    for i, p in enumerate(prescriptions, 1):
        raga_key = p["raga"].lower()
        yt_link  = YOUTUBE_LINKS.get(raga_key, "#")
        rasa_desc = rasa_meanings.get(p.get("rasa",""), p.get("rasa",""))
        conditions_str = ", ".join(c.replace("_"," ").title()
                                   for c in p.get("conditions",[])[:3])
        prescription_md += f\"\"\"
### {i}. Raag {p['raga']}
| Property | Value |
|---|---|
| \U0001f3ad Rasa (Emotional Colour) | **{rasa_desc}** |
| \u23f1 Recommended Duration | {p['duration_min']} minutes |
| \U0001f550 Best Time | {p.get('time','anytime').replace('_',' ').title()} |
| \U0001f48a Indicated For | {conditions_str} |
| \U0001f60a Valence | {'Positive' if p['valence'] > 0 else 'Negative'} ({p['valence']:+.1f}) |
| \u26a1 Arousal | {'High' if p['arousal'] > 0.5 else 'Moderate' if p['arousal'] > 0.25 else 'Low'} ({p['arousal']:.1f}) |

\u25b6\ufe0f **[Listen on YouTube]({yt_link})**

---
\"\"\"'''

new_block = '''    # Start HTML builder
    import markdown
    html_out = markdown.markdown(parsed['nlp_summary'])
    html_out = f"<h3>Recommended Music Sessions</h3>" + html_out
    
    for i, p in enumerate(prescriptions, 1):
        raga_key = p["raga"].lower()
        vid_id  = YOUTUBE_LINKS.get(raga_key, "")
        rasa_desc = rasa_meanings.get(p.get("rasa",""), p.get("rasa",""))
        conditions_str = ", ".join(c.replace("_"," ").title() for c in p.get("conditions",[])[:3])
        
        iframe = ""
        if len(vid_id) == 11:
            iframe = f'<iframe width="100%" height="220" src="https://www.youtube.com/embed/{vid_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius:8px; margin-top:10px;"></iframe>'
        else:
            iframe = f'<a href="https://www.youtube.com/results?search_query=Raag+{p["raga"]}+hindustani+classical" target="_blank" style="display:block; padding:10px; background:#e07b9e; color:white; text-align:center; border-radius:5px; text-decoration:none;">Listen on YouTube</a>'
            
        html_out += f\"\"\"
        <div style="background:#1e1e2f; padding:15px; border-radius:10px; margin-bottom:15px; border:1px solid #333;">
            <h4 style="margin-top:0; color:#7b9ee0; font-size:1.1rem;">{i}. Raag {p['raga']}</h4>
            <div style="font-size:0.9rem; color:#bbb; line-height:1.4;">
                <b>Rasa:</b> {rasa_desc} <br>
                <b>Indicated for:</b> {conditions_str} <br>
                <b>Duration:</b> {p['duration_min']} mins
            </div>
            {iframe}
        </div>
        \"\"\"
    prescription_md = html_out'''

text = text.replace(old_block, new_block)
with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

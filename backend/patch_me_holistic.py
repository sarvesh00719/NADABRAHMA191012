import re

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '''    # Map reviews by session
    rev_dict = {r.session_id: r for r in reviews}
    for i, s in enumerate(sessions[-5:], 1): # Last 5 sessions
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 10, f"Session {i}: {s.started_at.strftime('%Y-%m-%d %H:%M')} (Goal: {s.goal})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        rev = rev_dict.get(s.id)
        if rev and rev.draft_summary:
            clean_text = rev.draft_summary.replace('#', '').encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, clean_text)
        else:
            pdf.multi_cell(0, 6, "No clinical summary available for this session.")
        pdf.ln(5)'''

new_block = '''    # Generate holistic LLM Summary
    all_summaries = []
    rev_dict = {r.session_id: r for r in reviews}
    for s in sessions:
        rev = rev_dict.get(s.id)
        if rev and rev.draft_summary:
            all_summaries.append(f"Date: {s.started_at.strftime('%Y-%m-%d')} - {rev.draft_summary}")
    
    context = "\\n\\n".join(all_summaries)
    system_prompt = f\"\"\"You are a clinical psychotherapist generating a final holistic discharge/progress report for a patient.
Below are the individual summaries of their past {len(sessions)} sessions.
Please read them all and synthesize ONE comprehensive, professional clinical report.
Use professional clinical keywords (e.g., affect, presentation, cognitive themes, emotional regulation, trajectory).
Do NOT summarize them one by one. Write a cohesive narrative spanning their entire journey.
Include:
1. Presenting Problems & Initial State
2. Core Themes & Cognitive Patterns
3. Emotional Trends & Progress
4. Clinical Recommendations for the Future

Keep it to about 3-4 paragraphs.
Context:
{context}
\"\"\"
    
    try:
        from google import genai
        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=system_prompt,
        )
        holistic_report = response.text.strip()
    except Exception as e:
        holistic_report = "Error generating holistic report."

    # Write Holistic Report to PDF
    pdf.set_font("helvetica", "", 10)
    clean_text = holistic_report.replace('#', '').replace('*', '').encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, clean_text)
'''

text = text.replace(old_block, new_block)

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'w', encoding='utf-8') as f:
    f.write(text)

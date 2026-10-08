import re

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add export_my_data_pdf to me.py
export_fn = '''
from fastapi.responses import Response
import matplotlib.pyplot as plt
import io
import os
from fpdf import FPDF
from app.models.db_models import SessionReview, SessionModel, CheckIn

@router.get("/export/pdf")
def export_my_data_pdf(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 1. Gather data
    checkins = db.query(CheckIn).filter(CheckIn.user_id == user.id).order_by(CheckIn.created_at.asc()).all()
    sessions = db.query(SessionModel).filter(SessionModel.user_id == user.id).order_by(SessionModel.started_at.asc()).all()
    session_ids = [s.id for s in sessions]
    reviews = db.query(SessionReview).filter(SessionReview.session_id.in_(session_ids)).all()
    
    # 2. Generate Chart
    mood_map = {"worse": 1, "no_change": 2, "better": 3}
    energy_map = {"low": 1, "medium": 2, "high": 3}
    
    dates = []
    moods = []
    energies = []
    for c in checkins:
        m_val = mood_map.get(c.mood, 2)
        e_val = energy_map.get(c.energy, 2)
        dates.append(c.created_at.strftime("%Y-%m-%d"))
        moods.append(m_val)
        energies.append(e_val)
    
    chart_path = "temp_chart.png"
    if dates:
        plt.figure(figsize=(8, 4))
        plt.plot(dates[-10:], moods[-10:], marker='o', label='Mood (1=Worse, 3=Better)', color='#CA7C50')
        plt.plot(dates[-10:], energies[-10:], marker='s', label='Energy (1=Low, 3=High)', color='#7b9ee0')
        plt.title('Recent Emotional Trends')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
    
    # 3. Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 18)
    pdf.cell(0, 10, "Nadbrahma Clinical Therapy Report", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, f"Patient: {user.display_name or user.email}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Total Sessions: {len(sessions)}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=15, w=180)
        pdf.ln(5)
        os.remove(chart_path)
    
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "Clinical History & Key Findings", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    
    # Map reviews by session
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
        pdf.ln(5)
    
    pdf_bytes = pdf.output()
    
    return Response(content=bytes(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=therapy_report.pdf"})
'''

if 'def export_my_data_pdf' not in text:
    text = text + '\n' + export_fn

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'w', encoding='utf-8') as f:
    f.write(text)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.deps import get_current_user
from app.models import User, AuditEvent
from app.schemas import UserProfileResponse, ProfileUpdate

router = APIRouter(prefix="/me", tags=["me"])

@router.get("", response_model=UserProfileResponse)
def get_me(user: User = Depends(get_current_user)):
    return user

@router.patch("", response_model=UserProfileResponse)
def update_me(update_data: ProfileUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if update_data.display_name is not None:
        user.display_name = update_data.display_name
        
    if update_data.preferences is not None:
        prefs = user.preferences
        prefs_data = update_data.preferences.model_dump(exclude_unset=True)
        for k, v in prefs_data.items():
            setattr(prefs, k, v)
            
    db.commit()
    db.refresh(user)
    return user

@router.delete("/data", status_code=204)
def delete_my_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    event = AuditEvent(user_id=user.id, event_type="delete_data", target="all")
    db.add(event)
    
    db.delete(user)
    db.commit()
    return None
@router.get('/history')
def get_history(limit: int = 20, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models import SessionModel, SessionReview, CheckIn
    
    sessions = db.query(SessionModel).filter(SessionModel.user_id == user.id, SessionModel.status == 'reviewed').order_by(SessionModel.started_at.desc()).limit(limit).all()
    checkins = db.query(CheckIn).filter(CheckIn.user_id == user.id).order_by(CheckIn.created_at.desc()).limit(limit).all()
    
    items = []
    for s in sessions:
        duration = 0
        if s.ended_at and s.started_at:
            duration = int((s.ended_at - s.started_at).total_seconds())
        items.append({
            'type': 'session',
            'id': s.id,
            'date': s.started_at.isoformat(),
            'final_summary': s.review.final_summary if s.review else '',
            'topics': s.review.topics if s.review else [],
            'duration_sec': duration
        })
        
    for c in checkins:
        items.append({
            'type': 'check_in',
            'id': c.id,
            'date': c.created_at.isoformat(),
            'mood': c.mood
        })
        
    items.sort(key=lambda x: x['date'], reverse=True)
    return {'items': items[:limit]}

@router.delete('/data', status_code=204)
def delete_user_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models import CheckIn, SessionModel, Message, SessionReview, ActivityEvent, Feedback
    db.query(CheckIn).filter(CheckIn.user_id == user.id).delete()
    db.query(ActivityEvent).filter(ActivityEvent.user_id == user.id).delete()
    db.query(Feedback).filter(Feedback.user_id == user.id).delete()
    
    sessions = db.query(SessionModel).filter(SessionModel.user_id == user.id).all()
    for s in sessions:
        db.query(Message).filter(Message.session_id == s.id).delete()
        db.query(SessionReview).filter(SessionReview.session_id == s.id).delete()
        db.delete(s)
        
    db.commit()
    return None


from fastapi.responses import Response
import matplotlib.pyplot as plt
import io
import os
from fpdf import FPDF
from app.models import SessionReview, SessionModel, CheckIn

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
        plt.figure(figsize=(9, 4.5))
        # Plot ALL sessions over a numerical axis to avoid date overlap
        x_axis = list(range(1, len(moods) + 1))
        
        plt.plot(x_axis, moods, marker='o', linewidth=2, label='Mood (1=Worse, 3=Better)', color='#CA7C50')
        plt.plot(x_axis, energies, marker='s', linewidth=2, label='Energy (1=Low, 3=High)', color='#7b9ee0')
        
        plt.title(f'Comprehensive Emotional Trends (All {len(moods)} Sessions)')
        plt.xlabel('Session Number')
        
        # Sparse x-ticks if there are many sessions
        tick_interval = max(1, len(x_axis) // 10)
        plt.xticks(x_axis[::tick_interval])
        
        plt.yticks([1, 2, 3], ['Low / Worse', 'Neutral / No Change', 'High / Better'])
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # Calculate top topics for annotation
        all_topics = []
        for r in reviews:
            if r.topics:
                if isinstance(r.topics, list):
                    all_topics.extend(r.topics)
                elif isinstance(r.topics, str):
                    all_topics.extend([t.strip() for t in r.topics.split(',')])
                    
        if all_topics:
            from collections import Counter
            top_topics = [t[0] for t in Counter(all_topics).most_common(4)]
            topic_str = "Frequent Session Themes:\n" + "\n".join([f"- {t}" for t in top_topics])
            # Add text box to the chart clarifying the words/themes inside the sessions
            plt.text(1.02, 0.5, topic_str, transform=plt.gca().transAxes,
                     fontsize=10, verticalalignment='center',
                     bbox=dict(boxstyle='round', facecolor='#F3E8D6', alpha=0.8, edgecolor='#CA7C50'))
            
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
        plt.tight_layout(rect=[0, 0.05, 0.75, 1])
        plt.savefig(chart_path, dpi=200, bbox_inches='tight')
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
    
    # Generate holistic LLM Summary
    all_summaries = []
    rev_dict = {r.session_id: r for r in reviews}
    for s in sessions:
        rev = rev_dict.get(s.id)
        if rev and rev.draft_summary:
            all_summaries.append(f"Date: {s.started_at.strftime('%Y-%m-%d')} - {rev.draft_summary}")
    
    context = "\n\n".join(all_summaries)
    system_prompt = f"""You are a clinical psychotherapist generating a final holistic discharge/progress report for a patient.
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
"""
    
    try:
        from google import genai
        from app.config import settings
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=system_prompt,
        )
        holistic_report = response.text.strip()
    except Exception as e:
        holistic_report = f"Error generating holistic report: {str(e)}"

    # Write Holistic Report to PDF
    pdf.set_font("helvetica", "", 10)
    clean_text = holistic_report.replace('#', '').replace('*', '').encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, clean_text)

    
    pdf_bytes = pdf.output()
    
    return Response(content=bytes(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=therapy_report.pdf"})

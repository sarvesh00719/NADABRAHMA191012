import re

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_chart = '''    dates = []
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
        plt.close()'''

new_chart = '''    dates = []
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
        
        plt.yticks([1, 2, 3], ['Low/Worse', 'Neutral', 'High/Better'])
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(chart_path, dpi=200)
        plt.close()'''

old_llm = '''    try:
        from google import genai
        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=system_prompt,
        )
        holistic_report = response.text.strip()
    except Exception as e:
        holistic_report = "Error generating holistic report."'''

new_llm = '''    try:
        from google import genai
        from app.config import settings
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=system_prompt,
        )
        holistic_report = response.text.strip()
    except Exception as e:
        holistic_report = f"Error generating holistic report: {str(e)}"'''

text = text.replace(old_chart, new_chart)
text = text.replace(old_llm, new_llm)

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'w', encoding='utf-8') as f:
    f.write(text)

import re
with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# CSS
new_css = '''LIGHT_CSS = \"\"\"
:root {
  --bg-color: #FAF7F2;
  --panel-bg: #FFFFFF;
  --primary-color: #CA7C50;
  --text-color: #333333;
  --border-color: #E2E2E2;
}
body, .gradio-container {
  background-color: var(--bg-color) !important;
  color: var(--text-color) !important;
  font-family: 'Georgia', 'Times New Roman', serif !important;
}
.gr-panel, .gr-box, .gr-button {
  background-color: var(--panel-bg) !important;
  border: 1px solid var(--border-color) !important;
  color: var(--text-color) !important;
  border-radius: 12px !important;
}
.gr-button.primary {
  background-color: var(--primary-color) !important;
  color: white !important;
  font-weight: bold !important;
  border: none !important;
}
h1, h2, h3, h4, h5, h6, .gr-markdown {
  color: var(--text-color) !important;
}
\"\"\"
'''
text = re.sub(r'DARK_CSS = """[\s\S]*?"""', new_css, text)
text = text.replace('css=DARK_CSS', 'css=LIGHT_CSS')

# Chart Backgrounds
text = text.replace('#0f0f1a', '#FFFFFF')
text = text.replace('color="white"', 'color="#333333"')
text = text.replace('#333', '#E2E2E2')

# Emojis & Labels
text = text.replace('Analyse & Recommend', 'Analyze & Recommend')
text = text.replace('label="Prescription"', 'label="Recommendation Plan"')

text = text.replace('listen_radio = gr.Radio(["Yes", "Partly", "No"], label="Did you listen?")', 
                    'listen_radio = gr.Radio(["\U0001f3a7 Yes, I listened", "\u23ed\ufe0f I listened partly", "\u274c No, I skipped it"], label="Did you listen?")')
text = text.replace('feel_radio = gr.Radio(["Better", "No change", "Worse", "Skip"], label="How do you feel now?")',
                    'feel_radio = gr.Radio(["\U0001f60a Better", "\U0001f610 No change", "\U0001f614 Worse", "\u23ed\ufe0f Skip"], label="How do you feel now?")')
text = text.replace('style_radio = gr.Radio(["Yes", "Maybe", "No"], label="Would you choose this style again?")',
                    'style_radio = gr.Radio(["\U0001f44d Yes, it fits my style", "\U0001f914 Maybe", "\U0001f44e No, prefer something else"], label="Does this match your style?")')

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

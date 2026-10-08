with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to insert session_state
text = text.replace('symptom_input = gr.Textbox(', 'session_state = gr.State("")\n                symptom_input = gr.Textbox(')

# Change prescription_out to HTML
text = text.replace('prescription_out = gr.Markdown(label="Prescription")', 'prescription_out = gr.HTML(label="Prescription")')

# Add feedback group
feedback_ui = '''                with gr.Column(visible=False) as feedback_col:
                    gr.Markdown("### Optional Check-in")
                    listen_radio = gr.Radio(["Yes", "Partly", "No"], label="Did you listen?")
                    feel_radio = gr.Radio(["Better", "No change", "Worse", "Skip"], label="How do you feel now?")
                    style_radio = gr.Radio(["Yes", "Maybe", "No"], label="Would you choose this style again?")
                    submit_btn = gr.Button("Submit Feedback")
                    feedback_status = gr.Markdown()
'''

text = text.replace('session_out = gr.Markdown(label="Session Plan")', feedback_ui + '\n                session_out = gr.Markdown(label="Session Plan")')

# Update outputs in analyse_btn.click
text = text.replace('outputs=[prescription_out, session_out,', 'outputs=[prescription_out, feedback_col, session_out,')

# Add the feedback click event
feedback_click = '''
                submit_btn.click(
                    fn=submit_feedback,
                    inputs=[session_state, listen_radio, feel_radio, style_radio],
                    outputs=[feedback_status, feedback_col]
                )
'''
text = text.replace('# Fully clear everything', feedback_click + '\n                # Fully clear everything')

# Update demo.load
text = text.replace('demo.load(on_load, None, symptom_input)', 'demo.load(on_load, None, [symptom_input, session_state])')

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

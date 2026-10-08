import re
with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# I need to change what run_analysis returns.
old_run = '''def run_analysis(symptom_text, top_k):
    results = analyse_and_recommend(symptom_text, int(top_k))
    return results'''

new_run = '''def run_analysis(symptom_text, top_k):
    results = list(analyse_and_recommend(symptom_text, int(top_k)))
    # results[0] is prescription HTML
    # we need to insert gr.update(visible=True) as the 2nd return value
    results.insert(1, gr.update(visible=True))
    return tuple(results)'''

text = text.replace(old_run, new_run)
with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

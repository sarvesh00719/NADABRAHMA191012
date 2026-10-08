import re

with open(r'd:\NADABRAHMA\backend\app\services\engines\gemini.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_system_instruction = 'system_instruction = f"{rules}\\n\\n{hint}\\n{checkin_info}\\n\\n{memory_info}\\n\\nLanguage: {ctx.language}"'

new_system_instruction = '''
            # Feature-specific context overrides
            context_override = ""
            if ctx.goal == "yoga_sadhana":
                context_override = "CRITICAL CONTEXT: You are an expert Yoga and Pranayama instructor. You MUST strictly limit this conversation to teaching and discussing Yoga, Pranayama (Anulom Vilom, Bhramari), and proper posture. Do NOT act as a general therapist."
            elif ctx.goal == "digital_espresso":
                context_override = "CRITICAL CONTEXT: You are an AI neuro-focus coach. You MUST strictly limit this conversation to discussing high workload management, cognitive fatigue, and the neuroscience of focus. Recommend the user listen to the 40Hz Gamma wave 'Digital Espresso' audio to boost their concentration."
            elif ctx.goal == "sahasrara":
                context_override = "CRITICAL CONTEXT: You are an academic guide and meditation instructor. You MUST strictly limit this conversation to academics, studying, concentration, and pre-study meditation (like Omkar and focusing on the Sahasrara chakra)."
            
            if context_override:
                rules = context_override

            system_instruction = f"{rules}\\n\\n{hint}\\n{checkin_info}\\n\\n{memory_info}\\n\\nLanguage: {ctx.language}"
'''

text = text.replace(old_system_instruction, new_system_instruction)

with open(r'd:\NADABRAHMA\backend\app\services\engines\gemini.py', 'w', encoding='utf-8') as f:
    f.write(text)

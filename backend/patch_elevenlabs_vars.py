import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace voiceId hardcode with env variable
text = text.replace("const voiceId = '21m00Tcm4TlvDq8ikWAM'; // Rachel voice", "const voiceId = process.env.EXPO_PUBLIC_ELEVENLABS_VOICE_ID || '21m00Tcm4TlvDq8ikWAM';")
text = text.replace("model_id: 'eleven_turbo_v2_5'", "model_id: process.env.EXPO_PUBLIC_ELEVENLABS_MODEL_ID || 'eleven_turbo_v2_5'")

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

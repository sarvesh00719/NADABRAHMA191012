import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Update the initSession goal
old_init = '''body: JSON.stringify({ raga_id: "sahasrara", intent: "focus" })'''
new_init = '''body: JSON.stringify({ goal: "sahasrara", language: "en" })'''
text = text.replace(old_init, new_init)

# Remove the system prompt hack
old_chat = '''const contextText = "[SYSTEM: Guide them in a meditation focusing on the Sahasrara (top of head) and Ajna (mid-eyebrow). End by asking them to press 'Start Omkar'] " + userMsg.content;
      if (!sessionId) return;
      const res = await fetchApi("/sessions/" + sessionId + "/messages", {
        method: 'POST',
        body: JSON.stringify({ text: contextText, client_message_id: userMsg.id })
      });'''

new_chat = '''if (!sessionId) return;
      const res = await fetchApi("/sessions/" + sessionId + "/messages", {
        method: 'POST',
        body: JSON.stringify({ text: userMsg.content, client_message_id: userMsg.id })
      });'''
text = text.replace(old_chat, new_chat)

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

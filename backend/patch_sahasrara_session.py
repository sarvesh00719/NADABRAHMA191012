import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

old_effect = '''  // Hardcode a session ID for Sahasrara to keep it simple, or generate one
  const sessionId = 'sahasrara-temp';

  useEffect(() => {
    // Initial AI greeting
    const initialMsg: Message = {
        id: '1', role: 'assistant', 
        content: "Welcome to Sahasrara. I am here to guide your focus. What are you studying today, and how is your energy level?"
    };
    setMessages([initialMsg]);
    playSpeech(initialMsg.content);
    
    return () => {
      Speech.stop();
      if (playerRef.current) playerRef.current.pause();
    };
  }, []);'''

new_effect = '''  const [sessionId, setSessionId] = useState('');

  useEffect(() => {
    const initSession = async () => {
        try {
            const res = await fetchApi("/sessions", {
                method: "POST",
                body: JSON.stringify({ raga_id: "sahasrara", intent: "focus" })
            });
            setSessionId(res.id);
            
            const initialMsg: Message = {
                id: '1', role: 'assistant', 
                content: "Welcome to Sahasrara. I am here to guide your focus. What are you studying today, and how is your energy level?"
            };
            setMessages([initialMsg]);
            playSpeech(initialMsg.content);
        } catch (e) {
            console.error("Failed to create session", e);
        }
    };
    initSession();
    
    return () => {
      Speech.stop();
      if (playerRef.current) playerRef.current.pause();
    };
  }, []);'''

text = text.replace(old_effect, new_effect)
text = text.replace('const res = await fetchApi("/sessions/" + sessionId + "/messages", {', 'if (!sessionId) return;\n      const res = await fetchApi("/sessions/" + sessionId + "/messages", {')

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

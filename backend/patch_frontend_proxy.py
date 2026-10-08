import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

old_logic = '''const uri = FileSystem.cacheDirectory + 'tts_' + Date.now() + '.mp3';
      const voiceId = process.env.EXPO_PUBLIC_ELEVENLABS_VOICE_ID || '21m00Tcm4TlvDq8ikWAM';
      
      const downloadRes = await FileSystem.downloadAsync(
        'https://api.elevenlabs.io/v1/text-to-speech/' + voiceId,
        uri,
        {
          httpMethod: 'POST',
          headers: {
            'xi-api-key': apiKey,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: textToSpeak, model_id: process.env.EXPO_PUBLIC_ELEVENLABS_MODEL_ID || 'eleven_turbo_v2_5', voice_settings: { stability: 0.5, similarity_boost: 0.75 } })
        }
      );
      
      if (downloadRes.status !== 200) {
          console.error("ElevenLabs API Error:", downloadRes.status);
          Speech.speak(textToSpeak, {
            pitch: 1.0, rate: 1.0,
            onDone: () => setIsSpeaking(false)
          });
          return;
      }
      
      const player = createAudioPlayer(uri);'''

new_logic = '''const voiceId = process.env.EXPO_PUBLIC_ELEVENLABS_VOICE_ID || '21m00Tcm4TlvDq8ikWAM';
      
      // Call the proxy via GET
      const url = process.env.EXPO_PUBLIC_API_URL + "/sessions/tts?text=" + encodeURIComponent(textToSpeak) + "&voiceId=" + encodeURIComponent(voiceId) + "&apiKey=" + encodeURIComponent(apiKey);
      
      const player = createAudioPlayer(url);'''

text = text.replace(old_logic, new_logic)

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

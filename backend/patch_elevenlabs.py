import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace import
text = text.replace("import { useAudioRecorder, useAudioRecorderState, requestRecordingPermissionsAsync, RecordingPresets } from 'expo-audio';", "import { useAudioRecorder, useAudioRecorderState, requestRecordingPermissionsAsync, RecordingPresets, createAudioPlayer } from 'expo-audio';")

# Replace playSpeech
old_play = '''const playSpeech = (textToSpeak: string) => {
    Speech.stop();
    setIsSpeaking(true);
    Speech.speak(textToSpeak, {
      pitch: 1.0,
      rate: 1.0,
      onDone: () => setIsSpeaking(false),
      onError: () => setIsSpeaking(false),
      onStopped: () => setIsSpeaking(false)
    });
  };'''

new_play = '''const playerRef = useRef<any>(null);

  const playSpeech = async (textToSpeak: string) => {
    try {
      Speech.stop();
      if (playerRef.current) { playerRef.current.pause(); }
      setIsSpeaking(true);
      
      const apiKey = process.env.EXPO_PUBLIC_ELEVENLABS_API_KEY;
      if (!apiKey) {
        console.warn("ElevenLabs API Key missing. Falling back to native TTS.");
        Speech.speak(textToSpeak, {
          pitch: 1.0, rate: 1.0,
          onDone: () => setIsSpeaking(false),
          onError: () => setIsSpeaking(false),
          onStopped: () => setIsSpeaking(false)
        });
        return;
      }
      
      const uri = FileSystem.cacheDirectory + 'tts_' + Date.now() + '.mp3';
      const voiceId = '21m00Tcm4TlvDq8ikWAM'; // Rachel voice
      
      await FileSystem.downloadAsync(
        https://api.elevenlabs.io/v1/text-to-speech/ + voiceId,
        uri,
        {
          httpMethod: 'POST',
          headers: {
            'xi-api-key': apiKey,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: textToSpeak, model_id: 'eleven_turbo_v2_5', voice_settings: { stability: 0.5, similarity_boost: 0.75 } })
        }
      );
      
      const player = createAudioPlayer(uri);
      playerRef.current = player;
      player.play();
      setTimeout(() => setIsSpeaking(false), textToSpeak.length * 60);
    } catch (e) {
      console.error('ElevenLabs TTS Error:', e);
      setIsSpeaking(false);
    }
  };'''

text = text.replace(old_play, new_play)

# Add cleanup for playerRef in useEffect
text = text.replace("return () => { Speech.stop(); };", "return () => { Speech.stop(); if (playerRef.current) playerRef.current.pause(); };")

# Add pause for playerRef when sending message
text = text.replace("Speech.stop();\n    setIsSpeaking(false);", "Speech.stop();\n    if (playerRef.current) playerRef.current.pause();\n    setIsSpeaking(false);")

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

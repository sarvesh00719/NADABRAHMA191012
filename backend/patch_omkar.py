import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

old_omkar = '''  const playOmkarSequence = (count: number) => {
      if (count >= 5) {
          setOmkarMode(false);
          setOmkarCount(0);
          // Navigate to Lock-in mode or finish
          router.replace('/sahasrara');
          return;
      }
      setOmkarCount(count + 1);
      
      // Fallback: Use Expo Speech to slowly chant OM if no mp3 provided
      // In production, we'd play an actual audio file here
      Speech.speak("Ommmmmmmmmmmmmmmmmmmmmm", {
          pitch: 0.5, rate: 0.1,
          onDone: () => {
              setTimeout(() => playOmkarSequence(count + 1), 2000);
          }
      });
  };'''

new_omkar = '''  const omkarPlayerRef = useRef<any>(null);

  const playOmkarSequence = (count: number) => {
      if (count >= 5) {
          setOmkarMode(false);
          setOmkarCount(0);
          // Navigate to Lock-in mode or finish
          router.replace('/sahasrara');
          return;
      }
      setOmkarCount(count + 1);
      
      const omkarAsset = require('../../assets/audio/omkar.mp3');
      const omkarPlayer = createAudioPlayer(omkarAsset);
      omkarPlayerRef.current = omkarPlayer;
      
      const sub = omkarPlayer.addListener('playbackStatusUpdate', (status: any) => {
          if (status.didJustFinish) {
              sub.remove();
              setTimeout(() => playOmkarSequence(count + 1), 2000);
          }
      });
      omkarPlayer.play();
  };'''

text = text.replace(old_omkar, new_omkar)

# Also update the useEffect cleanup to stop omkarPlayer if component unmounts
cleanup_old = '''    return () => {
      Speech.stop();
      if (playerRef.current) playerRef.current.pause();
    };'''

cleanup_new = '''    return () => {
      Speech.stop();
      if (playerRef.current) playerRef.current.pause();
      if (omkarPlayerRef.current) omkarPlayerRef.current.pause();
    };'''

text = text.replace(cleanup_old, cleanup_new)

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

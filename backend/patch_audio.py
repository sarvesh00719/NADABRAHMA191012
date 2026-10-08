import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace imports
text = text.replace("import { Audio } from 'expo-av';", "import { useAudioRecorder, useAudioRecorderState, requestRecordingPermissionsAsync } from 'expo-audio';")

# Fix missing state imports if not present
if "useAudioRecorder" not in text:
    print("Replace failed?")

# Wait, let's just rewrite the specific components using regex.
# I will use a robust replacement for the Chat component state:
import_str = "import { useAudioRecorder, useAudioRecorderState } from 'expo-audio';"

# Remove Audio.Recording
text = re.sub(r'const \[recording, setRecording\] = useState<Audio\.Recording \| null>\(null\);', '', text)
text = re.sub(r'const \[isRecording, setIsRecording\] = useState\(false\);', '', text)

# Add useAudioRecorder hook right after useLocalSearchParams
text = re.sub(
    r'const \{ id \} = useLocalSearchParams\(\);',
    r'const { id } = useLocalSearchParams();\n  const recorder = useAudioRecorder({ sampleRate: 44100, numberOfChannels: 2 });\n  const recordingState = useAudioRecorderState(recorder);',
    text
)

# Update startRecording
new_start = '''const startRecording = async () => {
    try {
      const { status } = await requestRecordingPermissionsAsync();
      if (status === 'granted') {
        await recorder.prepareToRecordAsync();
        recorder.record();
      }
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };'''
text = re.sub(r'const startRecording = async \(\) => \{.*?^\s*};\n' , new_start + '\n', text, flags=re.MULTILINE|re.DOTALL)

# Update stopRecording
new_stop = '''const stopRecording = async () => {
    setTranscribing(true);
    try {
      await recorder.stop();
      const uri = recorder.uri;
      if (uri) {
        const token = await SecureStore.getItemAsync('token');
        const formData = new FormData();
        formData.append('file', { uri, name: 'audio.m4a', type: 'audio/m4a' } as any);
        const response = await fetch(process.env.EXPO_PUBLIC_API_URL + "/sessions/transcribe", {
          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + token },
          body: formData,
        });
        if (response.ok) {
          const data = await response.json();
          if (data.text) setText(data.text);
        }
      }
    } catch (error) {
      console.error('Failed to stop/transcribe', error);
    } finally {
      setTranscribing(false);
    }
  };'''
text = re.sub(r'const stopRecording = async \(\) => \{.*?^\s*};\n', new_stop + '\n', text, flags=re.MULTILINE|re.DOTALL)

# Replace UI isRecording references
text = text.replace('isRecording ? stopRecording : startRecording', 'recordingState.isRecording ? stopRecording : startRecording')
text = text.replace('isRecording ? styles.recordingBtn : null', 'recordingState.isRecording ? styles.recordingBtn : null')
text = text.replace('isRecording ? "Stop" : "Mic"', 'recordingState.isRecording ? "Stop" : "Mic"')
text = text.replace('loading || isRecording || transcribing', 'loading || recordingState.isRecording || transcribing')

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

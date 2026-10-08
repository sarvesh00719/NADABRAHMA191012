import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("import { useAudioRecorder, useAudioRecorderState, requestRecordingPermissionsAsync } from 'expo-audio';", "import { useAudioRecorder, useAudioRecorderState, requestRecordingPermissionsAsync, RecordingPresets } from 'expo-audio';")

text = text.replace("const recorder = useAudioRecorder({ sampleRate: 44100, numberOfChannels: 2 });", "const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);")

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

new_stop = '''const stopRecording = async () => {
    setTranscribing(true);
    try {
      await recorder.stop();
      let uri = recorder.uri;
      if (uri) {
        if (uri.startsWith('file://') === false && uri.startsWith('/') === true) {
            uri = 'file://' + uri;
        }
        
        const token = await SecureStore.getItemAsync('token');
        const base64Audio = await FileSystem.readAsStringAsync(uri, { encoding: FileSystem.EncodingType.Base64 });
        
        const response = await fetch(process.env.EXPO_PUBLIC_API_URL + "/sessions/transcribe", {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ audio_base64: base64Audio })
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data.text) {
              setText(data.text);
          }
        } else {
          console.error("Transcribe failed:", await response.text());
        }
      }
    } catch (error) {
      console.error('Failed to stop/transcribe', error);
    } finally {
      setTranscribing(false);
    }
  };'''

text = re.sub(r'const stopRecording = async \(\) => \{.*?^\s*};\n', new_stop + '\n', text, flags=re.MULTILINE|re.DOTALL)

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'w', encoding='utf-8') as f:
    f.write(text)

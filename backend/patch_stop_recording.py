import re

with open(r'd:\NADABRAHMA\mobile\app\session\[id].tsx', 'r', encoding='utf-8') as f:
    text = f.read()

if 'expo-file-system' not in text:
    text = text.replace("import * as SecureStore from 'expo-secure-store';", "import * as SecureStore from 'expo-secure-store';\nimport * as FileSystem from 'expo-file-system/legacy';")

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
        
        const response = await FileSystem.uploadAsync(
          process.env.EXPO_PUBLIC_API_URL + "/sessions/transcribe",
          uri,
          {
            httpMethod: 'POST',
            uploadType: FileSystem.FileSystemUploadType.MULTIPART,
            fieldName: 'file',
            mimeType: 'audio/m4a',
            headers: {
              'Authorization': 'Bearer ' + token,
            }
          }
        );
        
        if (response.status === 200) {
          const data = JSON.parse(response.body);
          if (data.text) {
              setText(data.text);
          }
        } else {
          console.error("Transcribe failed:", response.body);
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

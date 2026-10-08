import os
import shutil

src = r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx'
dst = r'd:\NADABRAHMA\mobile\app\sahasrara\yoga.tsx'
shutil.copyfile(src, dst)

with open(dst, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Omkar stuff with Yoga stuff
text = text.replace('goal: "sahasrara"', 'goal: "yoga_sadhana"')
text = text.replace('Start Omkar Chant', 'Start Yoga Camera')
text = text.replace('omkarMode', 'cameraMode')
text = text.replace('setOmkarMode', 'setCameraMode')
text = text.replace('const [omkarCount, setOmkarCount] = useState(0);', '')
text = text.replace('const omkarPlayerRef = useRef<any>(null);', '')
text = text.replace('playOmkarSequence', 'startCamera')
text = text.replace('Omkar Chanting...', 'Camera Active')

# We'll do a basic camera placeholder if expo-camera is installed
camera_import = \"\"\"import { CameraView, useCameraPermissions } from 'expo-camera';\"\"\"
text = text.replace(\"import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';\", \"import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';\\n\" + camera_import)

# Update the camera mode UI
old_ui = '''          <View style={styles.omkarContainer}>
              <Animated.Text style={[styles.lotus, { transform: [{ scale: waveAnim }] }]}>??</Animated.Text>
              <Text style={styles.omkarText}>Camera Active</Text>
              <Text style={styles.omkarCount}>{omkarCount} / 5</Text>
          </View>'''

new_ui = '''          <View style={{flex: 1, backgroundColor: 'black'}}>
              <CameraView style={{flex: 1}} facing="front" />
              <TouchableOpacity onPress={() => setCameraMode(false)} style={{padding: 20, backgroundColor: '#c0392b', alignItems: 'center'}}>
                <Text style={{color: 'white', fontWeight: 'bold'}}>Stop Camera</Text>
              </TouchableOpacity>
          </View>'''
text = text.replace(old_ui, new_ui)

# Add permission hook
text = text.replace('const [sessionId, setSessionId] = useState(\\'\\');', 'const [sessionId, setSessionId] = useState(\\'\\');\\n  const [permission, requestPermission] = useCameraPermissions();')

# Update startCamera
old_start = '''    const startCamera = (count: number) => {
        if (count >= 5) {
            setCameraMode(false);
            
            // Navigate to Lock-in mode or finish
            router.replace('/sahasrara');
            return;
        }
        
        
        const omkarAsset = process.env.EXPO_PUBLIC_API_URL + '/sessions/sahasrara/omkar';
        const omkarPlayer = createAudioPlayer(omkarAsset);
        
        
        const sub = omkarPlayer.addListener('playbackStatusUpdate', (status: any) => {
            if (status.didJustFinish) {
                sub.remove();
                setTimeout(() => startCamera(count + 1), 2000);
            }
        });
        omkarPlayer.play();
    };'''

new_start = '''    const startCamera = async () => {
        if (!permission?.granted) {
            await requestPermission();
        }
        setCameraMode(true);
    };'''
text = text.replace(old_start, new_start)

text = text.replace('startCamera(0);', 'startCamera();')
text = text.replace('?? Sahasrara Focus', '?? Yoga Sadhana')
text = text.replace('Start Yoga Camera ??', 'Start Yoga Camera ??')

with open(dst, 'w', encoding='utf-8') as f:
    f.write(text)

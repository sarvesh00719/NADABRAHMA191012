import re

src = r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx'
dst1 = r'd:\NADABRAHMA\mobile\app\sahasrara\yoga.tsx'
dst2 = r'd:\NADABRAHMA\mobile\app\sahasrara\espresso.tsx'

with open(src, 'r', encoding='utf-8') as f:
    text = f.read()

# --- Create Yoga ---
yoga = text
yoga = yoga.replace('goal: "sahasrara"', 'goal: "yoga_sadhana"')
yoga = yoga.replace('Start Omkar Chant', 'Start Yoga Camera')
yoga = yoga.replace('omkarMode', 'cameraMode')
yoga = yoga.replace('setOmkarMode', 'setCameraMode')
yoga = re.sub(r'const \[omkarCount, setOmkarCount\] = useState\(0\);\n', '', yoga)
yoga = yoga.replace('playOmkarSequence', 'startCamera')
yoga = yoga.replace('Omkar Chanting...', 'Camera Active')
yoga = yoga.replace(
    "import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';",
    "import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';\nimport { CameraView, useCameraPermissions } from 'expo-camera';"
)

uiRegex = re.compile(r'<View style=\{styles\.omkarContainer\}>[\s\S]*?</View>')
new_ui = '''<View style={{flex: 1, backgroundColor: 'black', height: 400}}>
            <CameraView style={{flex: 1}} facing="front" />
            <TouchableOpacity onPress={() => setCameraMode(false)} style={{padding: 20, backgroundColor: '#c0392b', alignItems: 'center'}}>
              <Text style={{color: 'white', fontWeight: 'bold'}}>Stop Camera</Text>
            </TouchableOpacity>
        </View>'''

yoga = uiRegex.sub(new_ui, yoga)
yoga = yoga.replace("const [sessionId, setSessionId] = useState('');", "const [sessionId, setSessionId] = useState('');\n  const [permission, requestPermission] = useCameraPermissions();")

funcRegex = re.compile(r'const startCamera = \(count: number\) => \{[\s\S]*?omkarPlayer\.play\(\);\n    \};')
new_func = '''const startCamera = async () => {
        if (!permission?.granted) {
            await requestPermission();
        }
        setCameraMode(true);
    };'''
yoga = funcRegex.sub(new_func, yoga)

yoga = yoga.replace('startCamera(0);', 'startCamera();')
yoga = yoga.replace('?? Sahasrara Focus', '?? Yoga Sadhana')
yoga = yoga.replace('Start Yoga Camera ??', 'Start Yoga Camera ??')

with open(dst1, 'w', encoding='utf-8') as f:
    f.write(yoga)

# --- Create Espresso ---
espresso = text
espresso = espresso.replace('goal: "sahasrara"', 'goal: "digital_espresso"')
espresso = espresso.replace('Start Omkar Chant ??', 'Start 40Hz Audio ?')
espresso = espresso.replace('?? Sahasrara Focus', '? Digital Espresso')
espresso = espresso.replace('??', '?')
espresso = espresso.replace('Omkar Chanting...', 'Playing 40Hz Tone...')
with open(dst2, 'w', encoding='utf-8') as f:
    f.write(espresso)

print("Done")

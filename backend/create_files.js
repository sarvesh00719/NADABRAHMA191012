const fs = require('fs');
const src = 'd:/NADABRAHMA/mobile/app/sahasrara/meditation.tsx';
const dst1 = 'd:/NADABRAHMA/mobile/app/sahasrara/yoga.tsx';
const dst2 = 'd:/NADABRAHMA/mobile/app/sahasrara/espresso.tsx';

let text = fs.readFileSync(src, 'utf8');

// --- Create Yoga ---
let yoga = text;
yoga = yoga.replace(/goal: "sahasrara"/g, 'goal: "yoga_sadhana"');
yoga = yoga.replace(/Start Omkar Chant/g, 'Start Yoga Camera');
yoga = yoga.replace(/omkarMode/g, 'cameraMode');
yoga = yoga.replace(/setOmkarMode/g, 'setCameraMode');
yoga = yoga.replace(/const \[omkarCount, setOmkarCount\] = useState\(0\);/g, '');
yoga = yoga.replace(/playOmkarSequence/g, 'startCamera');
yoga = yoga.replace(/Omkar Chanting.../g, 'Camera Active');
yoga = yoga.replace(
  "import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';",
  "import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';\nimport { CameraView, useCameraPermissions } from 'expo-camera';"
);

const old_ui = <View style={styles.omkarContainer}>
            <Animated.Text style={[styles.lotus, { transform: [{ scale: waveAnim }] }]}>??</Animated.Text>
            <Text style={styles.omkarText}>Camera Active</Text>
            <Text style={styles.omkarCount}>{omkarCount} / 5</Text>
        </View>;

const new_ui = <View style={{flex: 1, backgroundColor: 'black'}}>
            <CameraView style={{flex: 1}} facing="front" />
            <TouchableOpacity onPress={() => setCameraMode(false)} style={{padding: 20, backgroundColor: '#c0392b', alignItems: 'center'}}>
              <Text style={{color: 'white', fontWeight: 'bold'}}>Stop Camera</Text>
            </TouchableOpacity>
        </View>;

yoga = yoga.replace(old_ui, new_ui);
yoga = yoga.replace(/const \[sessionId, setSessionId\] = useState\(''\);/, "const [sessionId, setSessionId] = useState('');\n  const [permission, requestPermission] = useCameraPermissions();");

yoga = yoga.replace(/const startCamera = \(count: number\) => \{[\s\S]*?omkarPlayer\.play\(\);\n    \};/, const startCamera = async () => {
      if (!permission?.granted) {
          await requestPermission();
      }
      setCameraMode(true);
  };);
  
yoga = yoga.replace(/startCamera\(0\);/g, 'startCamera();');
yoga = yoga.replace(/?? Sahasrara Focus/g, '?? Yoga Sadhana');
yoga = yoga.replace(/Start Yoga Camera ??/g, 'Start Yoga Camera ??');
fs.writeFileSync(dst1, yoga, 'utf8');

// --- Create Espresso ---
let espresso = text;
espresso = espresso.replace(/goal: "sahasrara"/g, 'goal: "digital_espresso"');
espresso = espresso.replace(/Start Omkar Chant ??/g, 'Start 40Hz Audio ?');
espresso = espresso.replace(/?? Sahasrara Focus/g, '? Digital Espresso');
espresso = espresso.replace(/??/g, '?');
espresso = espresso.replace(/Omkar Chanting.../g, 'Playing 40Hz Tone...');
fs.writeFileSync(dst2, espresso, 'utf8');

console.log("Done");

import re

# Fix Yoga
with open(r'd:\NADABRAHMA\mobile\app\sahasrara\yoga.tsx', 'r', encoding='utf-8') as f:
    yoga = f.read()

yoga = yoga.replace("export default function SahasraraMeditation()", "export default function YogaSadhana()")
yoga = yoga.replace("import * as FileSystem from 'expo-file-system/legacy';", "import * as FileSystem from 'expo-file-system/legacy';\nimport { CameraView, useCameraPermissions } from 'expo-camera';")

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\yoga.tsx', 'w', encoding='utf-8') as f:
    f.write(yoga)


# Fix Espresso
with open(r'd:\NADABRAHMA\mobile\app\sahasrara\espresso.tsx', 'r', encoding='utf-8') as f:
    espresso = f.read()

espresso = espresso.replace("export default function SahasraraMeditation()", "export default function DigitalEspresso()")

# Update the audio reference to espresso.mp3 (we'll provide a placeholder or let user add it later)
espresso = espresso.replace("const omkarAsset = process.env.EXPO_PUBLIC_API_URL + '/sessions/sahasrara/omkar';", "const espressoAsset = process.env.EXPO_PUBLIC_API_URL + '/sessions/espresso/40hz';")
espresso = espresso.replace("createAudioPlayer(omkarAsset)", "createAudioPlayer(espressoAsset)")

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\espresso.tsx', 'w', encoding='utf-8') as f:
    f.write(espresso)

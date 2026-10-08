with open(r'd:\NADABRAHMA\mobile\app\(tabs)\profile.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("import * as FileSystem from 'expo-file-system';", "import * as FileSystem from 'expo-file-system/legacy';")

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\profile.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

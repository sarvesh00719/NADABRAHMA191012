import sys
sys.path.append(r'd:\NADABRAHMA\mobile\node_modules\expo-audio\build')
import os
for root, dirs, files in os.walk(r'd:\NADABRAHMA\mobile\node_modules\expo-audio\build'):
    for file in files:
        if file.endswith('.js') or file.endswith('.d.ts'):
            print(os.path.join(root, file))

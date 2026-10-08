import re
with open(r'd:\NADABRAHMA\mobile\app\(tabs)\profile.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Add SecureStore import
if "import * as SecureStore" not in text:
    text = text.replace("import * as Sharing from 'expo-sharing';", "import * as Sharing from 'expo-sharing';\nimport * as SecureStore from 'expo-secure-store';")

# Fix token retrieval
old_token_logic = "'Authorization': 'Bearer ' + (user?.token || '')"
new_token_logic = "'Authorization': 'Bearer ' + ((await SecureStore.getItemAsync('token')) || '')"
text = text.replace(old_token_logic, new_token_logic)

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\profile.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

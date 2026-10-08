import re

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\history.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure TouchableOpacity is imported
if 'TouchableOpacity' not in text:
    text = text.replace('import { View, Text, StyleSheet', 'import { View, Text, StyleSheet, TouchableOpacity')

if 'import { router }' not in text and 'useRouter' not in text:
    text = text.replace("import { fetchApi }", "import { useRouter } from 'expo-router';\nimport { fetchApi }")

# Add router hook to HistoryScreen
if 'const router = useRouter()' not in text:
    text = text.replace('const [sessions, setSessions] = useState([]);', 'const [sessions, setSessions] = useState([]);\n  const router = useRouter();')

# Replace <View style={[styles.card with <TouchableOpacity
text = text.replace('<View style={[styles.card, { backgroundColor: colors.surface }]}>', '<TouchableOpacity style={[styles.card, { backgroundColor: colors.surface }]} onPress={() => router.push(/session/review/)}>')

# Replace closing </View> of the card with </TouchableOpacity>
text = text.replace('''        ) : (
        <Text style={[styles.summaryText, { color: colors.textSecondary, fontStyle: 'italic' }]}>
          No summary generated yet.
        </Text>
      )}
    </View>''', '''        ) : (
        <Text style={[styles.summaryText, { color: colors.textSecondary, fontStyle: 'italic' }]}>
          No summary generated yet.
        </Text>
      )}
    </TouchableOpacity>''')

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\history.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

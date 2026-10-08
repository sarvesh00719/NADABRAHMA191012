import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\index.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Instead of exact match, just use regex to replace everything inside the ScrollView after sectionDesc
scrollRegex = re.compile(r'<Text style=\{styles\.sectionDesc\}>[\s\S]*?</Text>([\s\S]*?)</ScrollView>')

new_cards = '''
        <TouchableOpacity style={styles.card} onPress={() => router.push('/sahasrara/meditation')}>
          <Text style={styles.cardIcon}>??</Text>
          <View style={styles.cardText}>
            <Text style={styles.cardTitle}>Academics & Meditation</Text>
            <Text style={styles.cardDesc}>Pre-study focus & Omkar chants</Text>
          </View>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.card} onPress={() => router.push('/sahasrara/yoga')}>
          <Text style={styles.cardIcon}>??</Text>
          <View style={styles.cardText}>
            <Text style={styles.cardTitle}>Yoga Sadhana</Text>
            <Text style={styles.cardDesc}>Camera-based Pranayama guide</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.card} onPress={() => router.push('/sahasrara/espresso')}>
          <Text style={styles.cardIcon}>?</Text>
          <View style={styles.cardText}>
            <Text style={styles.cardTitle}>Digital Espresso</Text>
            <Text style={styles.cardDesc}>40Hz workload & burnout therapy</Text>
          </View>
        </TouchableOpacity>
'''

text = scrollRegex.sub(r'<Text style={styles.sectionDesc}>\n          Welcome to your hyper-focus engine. Before you study, let\'s bloom your potential with a guided meditation, then lock-in to your work.\n        </Text>' + new_cards + '\n      </ScrollView>', text)

# Fix the main icon at the top
text = re.sub(r'<Text style=\{styles\.icon\}>\?\?</Text>', '<Text style={styles.icon}>??</Text>', text)

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\index.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

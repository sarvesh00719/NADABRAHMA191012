import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\index.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

old_content = '''        <TouchableOpacity style={styles.card} onPress={() => router.push('/sahasrara/meditation')}>
          <Text style={styles.cardIcon}>??</Text>
          <View style={styles.cardText}>
            <Text style={styles.cardTitle}>Pre-Study Meditation</Text>
            <Text style={styles.cardDesc}>AI-guided Omkar & Third-Eye focus</Text>
          </View>
        </TouchableOpacity>
        
        <TouchableOpacity style={[styles.card, { opacity: 0.5 }]} disabled={true}>
          <Text style={styles.cardIcon}>??</Text>
          <View style={styles.cardText}>
            <Text style={styles.cardTitle}>Lock-In Mode (Coming Soon)</Text>
            <Text style={styles.cardDesc}>Camera-based distraction tracking</Text>
          </View>
        </TouchableOpacity>'''

new_content = '''        <TouchableOpacity style={styles.card} onPress={() => router.push('/sahasrara/meditation')}>
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
        </TouchableOpacity>'''

text = text.replace(old_content, new_content)

# Also fix the ?? icons to be real emojis
text = text.replace('<Text style={styles.icon}>??</Text>', '<Text style={styles.icon}>??</Text>')

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\index.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

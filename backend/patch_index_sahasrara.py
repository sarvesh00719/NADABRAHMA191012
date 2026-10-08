import re

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\index.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

sahasrara_ui = '''
        {/* Sahasrara Hub (Gen Z / Student) */}
        <TouchableOpacity style={styles.sahasraraBtn} onPress={() => router.push('/sahasrara')}>
          <View style={styles.sahasraraContent}>
            <Text style={styles.sahasraraIcon}>??</Text>
            <View>
              <Text style={styles.sahasraraTitle}>Sahasrara Hub</Text>
              <Text style={styles.sahasraraSubtitle}>Focus & Bloom</Text>
            </View>
          </View>
        </TouchableOpacity>
        
        {/* Grid Actions */}
'''
text = text.replace('{/* Grid Actions */}', sahasrara_ui)

styles_sahasrara = '''
  sahasraraBtn: { backgroundColor: '#2C3E50', padding: 20, borderRadius: 20, marginBottom: 20, shadowColor: '#000', shadowOpacity: 0.2, shadowOffset: { width: 0, height: 4 }, shadowRadius: 5, elevation: 5 },
  sahasraraContent: { flexDirection: 'row', alignItems: 'center' },
  sahasraraIcon: { fontSize: 40, marginRight: 15 },
  sahasraraTitle: { fontSize: 22, fontWeight: 'bold', color: '#F39C12' },
  sahasraraSubtitle: { fontSize: 14, color: '#ECF0F1', marginTop: 4 },
  actionGrid: {
'''
text = text.replace('  actionGrid: {', styles_sahasrara)

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\index.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

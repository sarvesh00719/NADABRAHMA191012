import re

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\history.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

old_render = '''      <View style={styles.cardHeader}>
        <MaterialCommunityIcons name="calendar-clock" size={20} color={colors.primary} />
        <Text style={[styles.dateText, { color: colors.textSecondary }]}>
          {new Date(item.started_at).toLocaleDateString()}
        </Text>
        <View style={[styles.badge, { backgroundColor: item.status === 'reviewed' ? '#DEF7EC' : '#FEF3C7' }]}>
          <Text style={[styles.badgeText, { color: item.status === 'reviewed' ? '#03543F' : '#92400E' }]}>
            {item.status.toUpperCase()}
          </Text>
        </View>
      </View>'''

new_render = '''      <View style={styles.cardHeader}>
        <MaterialCommunityIcons name="calendar-clock" size={20} color={colors.primary} />
        <Text style={[styles.dateText, { color: colors.textSecondary }]}>
          {new Date(item.started_at).toLocaleDateString()}
        </Text>
        <View style={[styles.badge, { backgroundColor: colors.primary + '20' }]}>
          <Text style={[styles.badgeText, { color: colors.primary }]}>
            {item.goal === 'yoga_sadhana' ? 'YOGA SADHANA' : 
             item.goal === 'digital_espresso' ? 'DIGITAL ESPRESSO' : 
             item.goal === 'sahasrara' ? 'ACADEMICS' : 'THERAPY'}
          </Text>
        </View>
        <View style={[styles.badge, { backgroundColor: item.status === 'reviewed' ? '#DEF7EC' : '#FEF3C7', marginLeft: 5 }]}>
          <Text style={[styles.badgeText, { color: item.status === 'reviewed' ? '#03543F' : '#92400E' }]}>
            {item.status.toUpperCase()}
          </Text>
        </View>
      </View>'''

text = text.replace(old_render, new_render)

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\history.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

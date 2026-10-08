import re

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the JSX mismatch
text = text.replace('</Text>\\n              <Text style={styles.omkarText}>', '</Animated.Text>\\n              <Text style={styles.omkarText}>')

# Wait, let's just do a direct regex or exact match
old_line = '<Animated.Text style={[styles.lotus, { transform: [{ scale: waveAnim }] }]}>??</Text>'
new_line = '<Animated.Text style={[styles.lotus, { transform: [{ scale: waveAnim }] }]}>??</Animated.Text>'
text = text.replace(old_line, new_line)

# Also fix other '??' that might have been mangled lotus emojis
text = text.replace('?? Sahasrara Focus', '?? Sahasrara Focus')
text = text.replace('Start Omkar Chant ??', 'Start Omkar Chant ??')

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\meditation.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

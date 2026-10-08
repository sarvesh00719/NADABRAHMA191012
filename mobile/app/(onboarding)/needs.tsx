import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, SafeAreaView } from 'react-native';
import { router } from 'expo-router';
import { colors } from '../../src/theme/colors';

const NEEDS = [
  'Stress', 'Feeling low',
  'Overthinking', 'Focus',
  'Sleep', 'Academic pressure',
  'Daily reflection', 'Just want to talk'
];

export default function Needs() {
  const [selected, setSelected] = useState<string[]>([]);

  const toggle = (n: string) => {
    if (selected.includes(n)) setSelected(selected.filter(x => x !== n));
    else setSelected([...selected, n]);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}><Text style={styles.headerText}>Back</Text></TouchableOpacity>
        <View style={styles.island} />
        <TouchableOpacity><Text style={styles.headerText}>Skip</Text></TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.title}>What would you like Nadbrahma to help you with?</Text>
        
        <View style={styles.grid}>
          {NEEDS.map(n => (
            <TouchableOpacity 
              key={n} 
              style={[styles.chip, selected.includes(n) && styles.chipSelected]}
              onPress={() => toggle(n)}
            >
              <Text style={[styles.chipText, selected.includes(n) && styles.chipTextSelected]}>{n}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.nextBtn} onPress={() => router.push('/(tabs)')}>
          <Text style={styles.nextBtnText}>Next</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: colors.background },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 20, paddingTop: 10, paddingBottom: 20 },
  headerText: { color: colors.textSecondary, fontSize: 16 },
  island: { width: 100, height: 30, backgroundColor: 'black', borderRadius: 15, opacity: 0 }, // fake island spacing
  
  container: { paddingHorizontal: 25, paddingTop: 20 },
  title: { fontSize: 32, fontWeight: 'bold', fontFamily: 'serif', color: colors.text, marginBottom: 40, lineHeight: 40 },
  
  grid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', gap: 15 },
  chip: { width: '47%', backgroundColor: colors.surface, borderRadius: 15, padding: 25, minHeight: 90, justifyContent: 'center', shadowColor: '#000', shadowOpacity: 0.02, shadowRadius: 5, elevation: 1 },
  chipSelected: { borderWidth: 2, borderColor: colors.primary, backgroundColor: colors.primaryLight },
  chipText: { color: colors.textSecondary, fontSize: 16, fontWeight: '500' },
  chipTextSelected: { color: colors.primary, fontWeight: '600' },

  footer: { padding: 20, paddingBottom: 40 },
  nextBtn: { backgroundColor: colors.primary, borderRadius: 15, paddingVertical: 18, alignItems: 'center' },
  nextBtnText: { color: colors.surface, fontSize: 16, fontWeight: '600' }
});

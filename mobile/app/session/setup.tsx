import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { router } from 'expo-router';
import { fetchApi } from '../../src/api/client';
import { colors } from '../../src/theme/colors';

export default function SessionSetup() {
  const [mood, setMood] = useState('okay');
  const [energy, setEnergy] = useState('medium');
  const [need, setNeed] = useState('calm');
  
  const startSession = async () => {
    try {
      await fetchApi('/check-ins', {
        method: 'POST',
        body: JSON.stringify({ mood, energy, need })
      });
      
      const session = await fetchApi('/sessions', {
        method: 'POST',
        body: JSON.stringify({ goal: 'reflection', language: 'en' })
      });
      
      router.replace(`/session/${session.id}`);
    } catch (e: any) {
      Alert.alert("Error", e.message);
    }
  };

  const renderChips = (options: string[], state: string, setter: (v: string) => void) => (
    <View style={styles.row}>
      {options.map(o => (
        <TouchableOpacity key={o} style={[styles.chip, state === o && styles.chipActive]} onPress={() => setter(o)}>
          <Text style={[styles.chipText, state === o && styles.chipTextActive]}>{o}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Check-in</Text>
      
      <Text style={styles.label}>Mood</Text>
      {renderChips(['great', 'good', 'okay', 'low', 'stressed', 'tired', 'restless'], mood, setMood)}
      
      <Text style={styles.label}>Energy</Text>
      {renderChips(['low', 'medium', 'high'], energy, setEnergy)}
      
      <Text style={styles.label}>Need</Text>
      {renderChips(['calm', 'sleep', 'focus', 'reflect', 'connect'], need, setNeed)}
      
      <TouchableOpacity style={styles.button} onPress={startSession}>
        <Text style={styles.buttonText}>Start Conversation</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: colors.background, paddingTop: 60 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, color: colors.text },
  label: { fontSize: 16, fontWeight: 'bold', marginTop: 10, marginBottom: 10, color: colors.text },
  row: { flexDirection: 'row', gap: 10, marginBottom: 20, flexWrap: 'wrap' },
  chip: { paddingHorizontal: 15, paddingVertical: 8, borderRadius: 20, backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border },
  chipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  chipText: { color: colors.text },
  chipTextActive: { color: colors.surface },
  button: { backgroundColor: colors.secondary, padding: 15, borderRadius: 8, alignItems: 'center', marginTop: 'auto' },
  buttonText: { color: colors.text, fontWeight: 'bold', fontSize: 16 }
});


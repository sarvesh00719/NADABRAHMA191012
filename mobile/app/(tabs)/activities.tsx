import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList } from 'react-native';
import { router } from 'expo-router';
import { colors } from '../../src/theme/colors';

const ACTIVITY_LIST = [
  { id: 'breathing', title: 'Box Breathing', type: 'Calming' },
  { id: 'grounding', title: '5-4-3-2-1 Grounding', type: 'Focus' },
  { id: 'winddown', title: 'Sleep Wind-down', type: 'Rest' }
];

export default function Activities() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Activities</Text>
      <FlatList 
        data={ACTIVITY_LIST}
        keyExtractor={i => i.id}
        renderItem={({item}) => (
          <TouchableOpacity style={styles.card} onPress={() => router.push(`/activity/${item.id}` as any)}>
            <Text style={styles.cardTitle}>{item.title}</Text>
            <Text style={styles.cardText}>{item.type}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: colors.background, paddingTop: 60 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, color: colors.text },
  card: { backgroundColor: colors.surface, padding: 20, borderRadius: 12, marginBottom: 15, shadowColor: '#000', shadowOpacity: 0.1, shadowRadius: 5, elevation: 3 },
  cardTitle: { fontSize: 18, fontWeight: 'bold', color: colors.text, marginBottom: 5 },
  cardText: { fontSize: 14, color: colors.textLight }
});

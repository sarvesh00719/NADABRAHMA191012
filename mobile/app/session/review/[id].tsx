import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Linking } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { fetchApi } from '../../../src/api/client';
import { colors } from '../../../src/theme/colors';

export default function SessionReview() {
  const { id } = useLocalSearchParams();
  const [summary, setSummary] = useState("Loading summary...");

  useEffect(() => {
    fetchApi(`/sessions/${id}`).then((res: any) => {
      setSummary(res.review?.draft_summary || "No summary available.");
    }).catch(e => {
      setSummary("Failed to load summary.");
    });
  }, [id]);

  const approve = async () => {
    try {
      await fetchApi(`/sessions/${id}/review`, {
        method: 'POST',
        body: JSON.stringify({ approve: true })
      });
      router.replace('/(tabs)/home');
    } catch(e) {
      console.error(e);
      router.replace('/(tabs)/home');
    }
  };

  const shareWithRaga = async () => {
    try {
      await fetchApi(`/sessions/${id}/review`, {
        method: 'POST',
        body: JSON.stringify({ approve: true })
      });
      router.replace(`/raga/${id}`);
    } catch(e) {
      router.replace(`/raga/${id}`);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Session Complete</Text>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Draft Summary</Text>
        <Text style={styles.cardText}>{summary}</Text>
      </View>

      <TouchableOpacity style={styles.button} onPress={approve}>
        <Text style={styles.buttonText}>Approve & Save</Text>
      </TouchableOpacity>
      
      <TouchableOpacity style={[styles.button, styles.buttonSecondary]} onPress={shareWithRaga}>
        <Text style={[styles.buttonText, { color: colors.text }]}>Find Music Therapy Ragas</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 20, backgroundColor: colors.background, paddingTop: 60 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, color: colors.text },
  card: { backgroundColor: colors.surface, padding: 20, borderRadius: 12, marginBottom: 20 },
  cardTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10, color: colors.text },
  cardText: { fontSize: 16, color: colors.textLight },
  button: { backgroundColor: colors.primary, padding: 15, borderRadius: 8, alignItems: 'center', marginBottom: 15 },
  buttonSecondary: { backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border },
  buttonText: { color: colors.surface, fontWeight: 'bold', fontSize: 16 }
});

import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, SafeAreaView, ScrollView } from 'react-native';
import { router } from 'expo-router';

export default function SahasraraHub() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.header}>
          <Text style={styles.icon}>🪷</Text>
          <Text style={styles.title}>Sahasrara</Text>
          <Text style={styles.subtitle}>The 1000-Petal Lotus of Focus</Text>
        </View>

        <Text style={styles.sectionDesc}>
          Welcome to your hyper-focus engine. Before you study, let\'s bloom your potential with a guided meditation, then lock-in to your work.
        </Text>
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

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#121212' },
  scroll: { padding: 20 },
  header: { alignItems: 'center', marginVertical: 40 },
  icon: { fontSize: 60, marginBottom: 10 },
  title: { fontSize: 32, fontWeight: 'bold', color: '#F39C12' },
  subtitle: { fontSize: 16, color: '#bdc3c7', marginTop: 5 },
  sectionDesc: { fontSize: 16, color: '#ecf0f1', textAlign: 'center', marginBottom: 40, lineHeight: 24 },
  card: { backgroundColor: '#1E2A38', padding: 20, borderRadius: 15, flexDirection: 'row', alignItems: 'center', marginBottom: 15 },
  cardIcon: { fontSize: 30, marginRight: 15 },
  cardText: { flex: 1 },
  cardTitle: { fontSize: 18, fontWeight: 'bold', color: '#fff' },
  cardDesc: { fontSize: 14, color: '#bdc3c7', marginTop: 5 }
});

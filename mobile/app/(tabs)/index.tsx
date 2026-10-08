import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { useTheme } from '../../src/theme/ThemeContext';
import { useTranslation } from 'react-i18next';

const MOODS = ['Great', 'Good', 'Okay', 'Low', 'Stressed', 'Tired', 'Restless'];

export default function Home() {
  const { colors } = useTheme();
  const styles = createStyles(colors);
  const [selectedMood, setSelectedMood] = useState('Great');
  const { t } = useTranslation();

  const startSession = () => {
    // Navigate to the setup screen or directly create session
    router.push('/session/setup');
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerLeft}>
            <Image source={require('../../assets/images/logo.png')} style={styles.logo} resizeMode="contain" />
            <View>
              <Text style={styles.greeting}>Good evening</Text>
              <Text style={styles.brandName}>Nadbrahma</Text>
            </View>
          </View>
          <View style={styles.profileIcon}>
            <Text style={{fontSize: 20}}>👤</Text>
          </View>
        </View>

        {/* Mood Card */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>How are you feeling today?</Text>
          <View style={styles.moodGrid}>
            {MOODS.map(m => (
              <TouchableOpacity 
                key={m} 
                style={[styles.moodChip, selectedMood === m && styles.moodChipSelected]}
                onPress={() => setSelectedMood(m)}
              >
                <Text style={[styles.moodText, selectedMood === m && styles.moodTextSelected]}>{m}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Main Action */}
        <TouchableOpacity style={styles.mainBtn} onPress={startSession}>
          <Text style={styles.mainBtnText}>Start a Session</Text>
        </TouchableOpacity>

        
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

        <View style={styles.actionGrid}>
          <TouchableOpacity style={styles.actionCard}>
            <Text style={styles.actionIcon}>💬</Text>
            <Text style={styles.actionTitle}>{t('Continue Previous Session')}</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionCard}>
            <Text style={styles.actionIcon}>🕒</Text>
            <Text style={styles.actionTitle}>{t('Daily reflection')}</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionCard}>
            <Text style={styles.actionIcon}>📈</Text>
            <Text style={styles.actionTitle}>{t('Explore Activities')}</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionCard}>
            <Text style={styles.actionIcon}>📅</Text>
            <Text style={styles.actionTitle}>{t('View History')}</Text>
          </TouchableOpacity>
        </View>

        {/* Privacy Note */}
        <View style={styles.privacyNote}>
          <Text style={styles.privacyIcon}>🛡️</Text>
          <Text style={styles.privacyText}>
            {t('Your reflections are yours. You control what is saved and shared.')}
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const createStyles = (colors: any) => StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: colors.background },
  container: { padding: 20, paddingBottom: 40 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 30, marginTop: 10 },
  headerLeft: { flexDirection: 'row', alignItems: 'center' },
  logo: { width: 55, height: 55, marginRight: 12 },
  greeting: { fontSize: 14, color: colors.textSecondary },
  brandName: { fontSize: 20, fontWeight: 'bold', fontFamily: 'serif', color: colors.text },
  profileIcon: { width: 40, height: 40, borderRadius: 20, backgroundColor: colors.surface, justifyContent: 'center', alignItems: 'center', shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 5, elevation: 2 },
  
  card: { backgroundColor: colors.surface, borderRadius: 20, padding: 25, marginBottom: 20, shadowColor: '#000', shadowOpacity: 0.03, shadowRadius: 10, elevation: 2 },
  cardTitle: { fontSize: 24, fontWeight: 'bold', fontFamily: 'serif', color: colors.text, marginBottom: 20, textAlign: 'center' },
  moodGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: 10 },
  moodChip: { backgroundColor: colors.primaryLight, paddingVertical: 10, paddingHorizontal: 18, borderRadius: 20 },
  moodChipSelected: { backgroundColor: colors.primary },
  moodText: { color: colors.textSecondary, fontSize: 15, fontWeight: '500' },
  moodTextSelected: { color: colors.surface, fontWeight: '600' },

  mainBtn: { backgroundColor: colors.primary, borderRadius: 15, paddingVertical: 18, alignItems: 'center', marginBottom: 25 },
  mainBtnText: { color: colors.surface, fontSize: 16, fontWeight: '600' },


  sahasraraBtn: { backgroundColor: '#2C3E50', padding: 20, borderRadius: 20, marginBottom: 20, shadowColor: '#000', shadowOpacity: 0.2, shadowOffset: { width: 0, height: 4 }, shadowRadius: 5, elevation: 5 },
  sahasraraContent: { flexDirection: 'row', alignItems: 'center' },
  sahasraraIcon: { fontSize: 40, marginRight: 15 },
  sahasraraTitle: { fontSize: 22, fontWeight: 'bold', color: '#F39C12' },
  sahasraraSubtitle: { fontSize: 14, color: '#ECF0F1', marginTop: 4 },
  actionGrid: {
 flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', gap: 15, marginBottom: 30 },
  actionCard: { width: '47%', backgroundColor: colors.surface, borderRadius: 20, padding: 20, height: 130, justifyContent: 'space-between', shadowColor: '#000', shadowOpacity: 0.03, shadowRadius: 10, elevation: 2 },
  actionIcon: { fontSize: 24, color: colors.primary },
  actionTitle: { fontSize: 15, fontWeight: '500', color: colors.text },

  privacyNote: { flexDirection: 'row', alignItems: 'center', backgroundColor: 'transparent', paddingHorizontal: 10 },
  privacyIcon: { fontSize: 18, marginRight: 10 },
  privacyText: { flex: 1, fontSize: 13, color: colors.textSecondary, lineHeight: 18 }
});



import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, SafeAreaView, ActivityIndicator } from 'react-native';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../../src/theme/ThemeContext';
import { useRouter } from 'expo-router';
import { fetchApi } from '../../src/api/client';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function History() {
  const { t } = useTranslation();
  const { colors } = useTheme();
  const [sessions, setSessions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const res = await fetchApi('/sessions/');
      setSessions(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const renderItem = ({ item }: { item: any }) => (
    <TouchableOpacity style={[styles.card, { backgroundColor: colors.surface }]} onPress={() => router.push(`/session/review/${item.id}`)}>
      <View style={styles.cardHeader}>
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
      </View>
      
      {item.draft_summary ? (
        <Text style={[styles.summaryText, { color: colors.text }]} numberOfLines={3}>
          {item.draft_summary.replace(/#/g, '')}
        </Text>
      ) : (
        <Text style={[styles.summaryText, { color: colors.textSecondary, fontStyle: 'italic' }]}>
          No summary generated yet.
        </Text>
      )}

      {item.topics && item.topics.length > 0 && (
        <View style={styles.topicsRow}>
          {item.topics.map((topic: string, idx: number) => (
            <View key={idx} style={[styles.topicChip, { backgroundColor: colors.primaryLight }]}>
              <Text style={[styles.topicText, { color: colors.text }]}>{topic}</Text>
            </View>
          ))}
        </View>
      )}
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={[styles.safeArea, { backgroundColor: colors.background }]}>
      <View style={styles.container}>
        <Text style={[styles.title, { color: colors.text }]}>{t('History')}</Text>
        <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
          You have completed {sessions.length} sessions.
        </Text>

        {loading ? (
          <ActivityIndicator size="large" color={colors.primary} style={{ marginTop: 50 }} />
        ) : (
          <FlatList
            data={sessions}
            keyExtractor={s => s.id}
            renderItem={renderItem}
            contentContainerStyle={styles.list}
            showsVerticalScrollIndicator={false}
          />
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1 },
  container: { flex: 1, padding: 20 },
  title: { fontSize: 32, fontWeight: 'bold', fontFamily: 'serif' },
  subtitle: { fontSize: 16, marginTop: 4, marginBottom: 20 },
  list: { paddingBottom: 40 },
  
  card: { 
    borderRadius: 16, 
    padding: 16, 
    marginBottom: 16,
    shadowColor: '#000', 
    shadowOpacity: 0.03, 
    shadowRadius: 10, 
    elevation: 2 
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  dateText: {
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
    flex: 1,
  },
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  badgeText: {
    fontSize: 10,
    fontWeight: 'bold',
  },
  summaryText: {
    fontSize: 15,
    lineHeight: 22,
    marginBottom: 12,
  },
  topicsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  topicChip: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 12,
  },
  topicText: {
    fontSize: 12,
    fontWeight: '500',
  }
});

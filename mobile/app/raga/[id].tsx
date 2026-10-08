import React from 'react';
import { StyleSheet, SafeAreaView, TouchableOpacity, Text, View } from 'react-native';
import { WebView } from 'react-native-webview';
import { router, useLocalSearchParams } from 'expo-router';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useTheme } from '../../src/theme/ThemeContext';
import { useTranslation } from 'react-i18next';

export default function RagaWebView() {
  const { id } = useLocalSearchParams();
  const { colors } = useTheme();
  const { t } = useTranslation();
  
  // The localtunnel URL for the Gradio app
  const ipMatch = (process.env.EXPO_PUBLIC_API_URL || "").match(/http:\/\/(.*?):/);
  const ip = ipMatch ? ipMatch[1] : "192.168.1.6";
  const gradioUrl = `http://${ip}:7860/?session_id=${id}`;

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={[styles.header, { borderBottomColor: colors.border }]}>
        <TouchableOpacity onPress={() => router.replace('/(tabs)/home')} style={styles.backButton}>
          <MaterialCommunityIcons name="arrow-left" size={24} color={colors.text} />
          <Text style={[styles.backText, { color: colors.text }]}>{t('Back to Home')}</Text>
        </TouchableOpacity>
      </View>
      
      <WebView 
        source={{ 
          uri: gradioUrl,
          headers: {
            'Bypass-Tunnel-Reminder': 'true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
          }
        }}
        style={styles.webview}
        startInLoadingState={true}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 30, // For notch
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  backText: {
    fontSize: 16,
    marginLeft: 8,
    fontWeight: '600',
  },
  webview: {
    flex: 1,
  }
});

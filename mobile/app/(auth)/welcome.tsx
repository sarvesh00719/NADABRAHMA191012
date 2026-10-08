import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Platform, Modal } from 'react-native';
import { router } from 'expo-router';
import { colors } from '../../src/theme/colors';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { useTranslation } from 'react-i18next';
import { saveLanguage } from '../../src/i18n';

export default function Welcome() {
  const { t, i18n } = useTranslation();
  const [langModal, setLangModal] = useState(false);

  const switchLanguage = (lang: string) => {
    saveLanguage(lang);
    i18n.changeLanguage(lang);
    setLangModal(false);
  };

  const getLangLabel = () => {
    if (i18n.language === 'hi') return 'HI';
    if (i18n.language === 'mr') return 'MR';
    return 'EN';
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <View style={styles.container}>
        
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerLeft}>
            <Image source={require('../../assets/images/logo.png')} style={styles.headerLogo} resizeMode="contain" />
            <Text style={styles.headerTitle}>{t('Nadbrahma')}</Text>
          </View>
          <TouchableOpacity style={styles.langButton} onPress={() => setLangModal(true)}>
            <Text style={styles.langText}>{getLangLabel()} ∨</Text>
          </TouchableOpacity>
        </View>

        {/* Main Content */}
        <View style={styles.mainContent}>
          {/* Concentric Circles Graphic */}
          <View style={styles.graphicContainer}>
            <View style={[styles.circle, styles.circle1]}>
              <View style={[styles.circle, styles.circle2]}>
                <View style={[styles.circle, styles.circle3]}>
                  <View style={styles.circleCore} />
                </View>
              </View>
            </View>
          </View>

          {/* Main Logo */}
          <Image source={require('../../assets/images/logo.png')} style={styles.mainLogo} resizeMode="contain" />

          {/* Welcome Text */}
          <Text style={styles.welcomeTitle}>{t('Welcome to')}{'\n'}{t('Nadbrahma')}</Text>
          <Text style={styles.subtitle}>{t('A space to pause, reflect, and talk.')}</Text>
        </View>

        {/* Footer Buttons */}
        <View style={styles.footer}>
          <TouchableOpacity style={styles.primaryButton} onPress={() => router.push('/(auth)/register')}>
            <Text style={styles.primaryButtonText}>{t('Get Started')}</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.secondaryButton} onPress={() => router.push('/(auth)/login')}>
            <Text style={styles.secondaryButtonText}>{t('I already have an account')}</Text>
          </TouchableOpacity>
        </View>

        {/* Language Modal */}
        <Modal visible={langModal} transparent animationType="fade">
          <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setLangModal(false)}>
            <View style={styles.modalContent}>
              <TouchableOpacity style={styles.modalItem} onPress={() => switchLanguage('en')}><Text style={styles.modalText}>English</Text></TouchableOpacity>
              <TouchableOpacity style={styles.modalItem} onPress={() => switchLanguage('hi')}><Text style={styles.modalText}>Hindi</Text></TouchableOpacity>
              <TouchableOpacity style={styles.modalItem} onPress={() => switchLanguage('mr')}><Text style={styles.modalText}>Marathi</Text></TouchableOpacity>
            </View>
          </TouchableOpacity>
        </Modal>

      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#FAF7F2',
  },
  container: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: Platform.OS === 'android' ? 40 : 10,
    paddingBottom: 30,
    justifyContent: 'space-between',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 10,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerLogo: {
    width: 45,
    height: 45,
    marginRight: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1A202C',
    fontFamily: Platform.OS === 'ios' ? 'Georgia' : 'serif',
  },
  langButton: {
    borderWidth: 1,
    borderColor: '#CA7C50',
    borderRadius: 20,
    paddingVertical: 6,
    paddingHorizontal: 12,
  },
  langText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#1A202C',
  },
  mainContent: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  graphicContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 40,
    height: 200,
  },
  circle: {
    borderWidth: 1,
    borderColor: 'rgba(202, 124, 80, 0.3)',
    borderRadius: 999,
    alignItems: 'center',
    justifyContent: 'center',
  },
  circle1: { width: 220, height: 220 },
  circle2: { width: 160, height: 160, borderColor: 'rgba(100, 120, 130, 0.3)' },
  circle3: { width: 100, height: 100, borderColor: 'rgba(202, 124, 80, 0.4)' },
  circleCore: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(202, 124, 80, 0.2)',
  },
  mainLogo: {
    width: 200,
    height: 200,
    marginBottom: 24,
  },
  welcomeTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#0A142F',
    textAlign: 'center',
    fontFamily: Platform.OS === 'ios' ? 'Georgia' : 'serif',
    lineHeight: 40,
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 15,
    color: '#556070',
    textAlign: 'center',
  },
  footer: {
    width: '100%',
    paddingBottom: 20,
  },
  primaryButton: {
    backgroundColor: '#CA7C50',
    borderRadius: 16,
    paddingVertical: 18,
    alignItems: 'center',
    marginBottom: 16,
  },
  primaryButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  secondaryButton: {
    paddingVertical: 12,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: '#556070',
    fontSize: 14,
    fontWeight: '500',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 16,
    width: 250,
    overflow: 'hidden',
  },
  modalItem: {
    paddingVertical: 18,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    alignItems: 'center',
  },
  modalText: {
    fontSize: 16,
    fontWeight: '500',
    color: '#1A202C',
  },
});

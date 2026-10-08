import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Switch, Modal } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuth } from '../../src/auth/AuthContext';
import { useTranslation } from 'react-i18next';
import { saveLanguage } from '../../src/i18n';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useTheme } from '../../src/theme/ThemeContext';
import * as FileSystem from 'expo-file-system/legacy';
import * as Sharing from 'expo-sharing';
import * as SecureStore from 'expo-secure-store';
import { Alert } from 'react-native';


export default function Profile() {
  const { user, logout } = useAuth();
  const { t, i18n } = useTranslation();
  const { isDarkMode, setDarkMode, colors } = useTheme();
  
  const [langModal, setLangModal] = useState(false);
  const [optionalObs, setOptionalObs] = useState(false);

  const handleExport = async () => {
    try {
      Alert.alert('Generating Report', 'Please wait while we compile your therapy history into a PDF...');
      
      const fileUri = FileSystem.documentDirectory + 'Nadbrahma_Clinical_Report.pdf';
      
      const { uri, status } = await FileSystem.downloadAsync(
        `${process.env.EXPO_PUBLIC_API_URL}/me/export/pdf`,
        fileUri,
        {
          headers: {
            'Authorization': 'Bearer ' + ((await SecureStore.getItemAsync('token')) || '')
          }
        }
      );
      
      if (status !== 200) throw new Error('Failed to download report');
      
      const isSharingAvailable = await Sharing.isAvailableAsync();
      if (isSharingAvailable) {
        await Sharing.shareAsync(uri, { UTI: '.pdf', mimeType: 'application/pdf' });
      } else {
        Alert.alert('Success', 'PDF saved to documents');
      }
    } catch (e) {
      console.error(e);
      Alert.alert('Export Failed', 'Unable to generate PDF report.');
    }
  };


  const switchLanguage = (lang: string) => {
    saveLanguage(lang);
    i18n.changeLanguage(lang);
    setLangModal(false);
  };

  const getLangLabel = () => {
    if (i18n.language === 'hi') return 'Hindi';
    if (i18n.language === 'mr') return 'Marathi';
    return 'English';
  };

  const menuItems = [
    { icon: 'translate', label: 'Language', isButton: true, action: () => setLangModal(true) },
    { icon: 'chat-outline', label: 'Conversation preferences', isButton: true },
    { icon: 'microphone-outline', label: 'Voice settings', isButton: true },
    { icon: 'camera-outline', label: 'Camera permissions', isButton: true },
    { icon: 'shield-outline', label: 'Data & Privacy', isButton: true },
    { icon: 'history', label: 'History', isButton: true },
    { icon: 'bell-outline', label: 'Notifications', isButton: true },
    { icon: 'download-outline', label: 'Export my data', isButton: true, action: handleExport },
    { icon: 'help-circle-outline', label: 'Help & Support', isButton: true },
    { icon: 'information-outline', label: 'About Nadbrahma', isButton: true },
  ];

  return (
    <SafeAreaView style={[styles.safeArea, { backgroundColor: colors.background }]}>
      <ScrollView contentContainerStyle={styles.container}>
        
        <View style={styles.header}>
          <Text style={[styles.title, { color: colors.text }]}>{t('Profile')}</Text>
          <Text style={[styles.subtitle, { color: colors.textSecondary }]}>{user?.display_name || user?.email}</Text>
        </View>

        <View style={[styles.card, { backgroundColor: colors.surface }]}>
          {menuItems.map((item, index) => (
            <TouchableOpacity 
              key={index} 
              style={[styles.menuItem, index !== menuItems.length - 1 && { borderBottomWidth: 1, borderBottomColor: colors.border }]}
              onPress={item.action}
              activeOpacity={0.7}
            >
              <View style={styles.menuLeft}>
                <MaterialCommunityIcons name={item.icon as any} size={22} color={colors.primary} style={styles.menuIcon} />
                <Text style={[styles.menuText, { color: colors.text }]}>{t(item.label)}</Text>
              </View>
              {item.label === 'Language' ? (
                <View style={styles.menuRight}>
                  <Text style={[styles.valueText, { color: colors.textSecondary }]}>{getLangLabel()}</Text>
                  <MaterialCommunityIcons name="chevron-right" size={20} color={colors.textSecondary} />
                </View>
              ) : (
                <MaterialCommunityIcons name="chevron-right" size={20} color={colors.textSecondary} />
              )}
            </TouchableOpacity>
          ))}

          <View style={[styles.menuItem, { borderTopWidth: 1, borderTopColor: colors.border, marginTop: 8, paddingTop: 24 }]}>
            <View style={styles.menuLeft}>
              <MaterialCommunityIcons name="moon-waning-crescent" size={22} color={colors.primary} style={styles.menuIcon} />
              <Text style={[styles.menuText, { color: colors.text }]}>{t('Dark mode')}</Text>
            </View>
            <Switch 
              value={isDarkMode} 
              onValueChange={setDarkMode}
              trackColor={{ false: colors.border, true: colors.primary }}
              thumbColor="#FFFFFF"
            />
          </View>
          
          <View style={[styles.menuItem, { borderBottomWidth: 1, borderBottomColor: colors.border }]}>
            <View style={styles.menuLeft}>
              <MaterialCommunityIcons name="database-outline" size={22} color={colors.primary} style={styles.menuIcon} />
              <Text style={[styles.menuText, { color: colors.text }]}>{t('Optional observation')}</Text>
            </View>
            <Switch 
              value={optionalObs} 
              onValueChange={setOptionalObs}
              trackColor={{ false: colors.border, true: colors.primary }}
              thumbColor="#FFFFFF"
            />
          </View>
        </View>

        <TouchableOpacity style={styles.logoutButton} onPress={logout}>
          <MaterialCommunityIcons name="logout" size={20} color={colors.error} style={styles.menuIcon} />
          <Text style={[styles.logoutText, { color: colors.error }]}>{t('Log Out')}</Text>
        </TouchableOpacity>

      </ScrollView>

      {/* Language Modal */}
      <Modal visible={langModal} transparent animationType="fade">
        <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setLangModal(false)}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <Text style={[styles.modalTitle, { color: colors.text, borderBottomColor: colors.border }]}>{t('Select Language')}</Text>
            <TouchableOpacity style={[styles.modalItem, { borderBottomColor: colors.border }]} onPress={() => switchLanguage('en')}><Text style={[styles.modalText, { color: colors.text }]}>English</Text></TouchableOpacity>
            <TouchableOpacity style={[styles.modalItem, { borderBottomColor: colors.border }]} onPress={() => switchLanguage('hi')}><Text style={[styles.modalText, { color: colors.text }]}>Hindi (हिंदी)</Text></TouchableOpacity>
            <TouchableOpacity style={[styles.modalItem, { borderBottomColor: colors.border }]} onPress={() => switchLanguage('mr')}><Text style={[styles.modalText, { color: colors.text }]}>Marathi (मराठी)</Text></TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1 },
  container: { padding: 20, paddingBottom: 40 },
  header: { marginBottom: 24, marginTop: 10 },
  title: { fontSize: 32, fontWeight: 'bold', fontFamily: 'serif' },
  subtitle: { fontSize: 16, marginTop: 4 },
  
  card: { 
    borderRadius: 20, 
    paddingHorizontal: 16,
    paddingVertical: 8,
    shadowColor: '#000', 
    shadowOpacity: 0.03, 
    shadowRadius: 10, 
    elevation: 2 
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 16,
  },
  menuLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  menuIcon: {
    marginRight: 14,
  },
  menuText: {
    fontSize: 16,
    fontWeight: '400',
  },
  menuRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  valueText: {
    fontSize: 14,
    marginRight: 8,
  },
  
  logoutButton: { 
    flexDirection: 'row',
    backgroundColor: '#FEE2E2', 
    padding: 18, 
    borderRadius: 16, 
    alignItems: 'center', 
    justifyContent: 'center',
    marginTop: 30 
  },
  logoutText: { fontWeight: 'bold', fontSize: 16 },

  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.4)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    borderRadius: 20,
    width: '80%',
    overflow: 'hidden',
    paddingVertical: 10,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    paddingVertical: 15,
    borderBottomWidth: 1,
  },
  modalItem: {
    paddingVertical: 18,
    borderBottomWidth: 1,
    alignItems: 'center',
  },
  modalText: {
    fontSize: 16,
    fontWeight: '500',
  },
});

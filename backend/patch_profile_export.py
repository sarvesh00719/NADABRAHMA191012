import re

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\profile.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Add imports for FileSystem and Sharing
imports = """import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';
import { Alert } from 'react-native';
"""
if 'expo-file-system' not in text:
    text = text.replace("import { useTheme } from '../../src/theme/ThemeContext';", "import { useTheme } from '../../src/theme/ThemeContext';\n" + imports)

# Find menuItems
old_export = "{ icon: 'download-outline', label: 'Export my data', isButton: true },"

# Add export handler function
export_handler = """
  const handleExport = async () => {
    try {
      Alert.alert('Generating Report', 'Please wait while we compile your therapy history into a PDF...');
      
      const fileUri = FileSystem.documentDirectory + 'Nadbrahma_Clinical_Report.pdf';
      
      const { uri, status } = await FileSystem.downloadAsync(
        `${process.env.EXPO_PUBLIC_API_URL}/users/export/pdf`,
        fileUri,
        {
          headers: {
            'Authorization': 'Bearer ' + (user?.token || '')
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
"""

if 'const handleExport = async () => {' not in text:
    text = text.replace('const [optionalObs, setOptionalObs] = useState(false);', 'const [optionalObs, setOptionalObs] = useState(false);\n' + export_handler)

text = text.replace(old_export, "{ icon: 'download-outline', label: 'Export my data', isButton: true, action: handleExport },")

with open(r'd:\NADABRAHMA\mobile\app\(tabs)\profile.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

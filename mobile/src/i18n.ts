import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import AsyncStorage from '@react-native-async-storage/async-storage';

const resources = {
  "en": {
    "translation": {
      "Welcome to": "Welcome to",
      "Nadbrahma": "Nadbrahma",
      "A space to pause, reflect, and talk.": "A space to pause, reflect, and talk.",
      "Get Started": "Get Started",
      "I already have an account": "I already have an account",
      "Good evening": "Good evening",
      "How are you feeling today?": "How are you feeling today?",
      "Start a Session": "Start a Session",
      "Profile": "Profile",
      "Language": "Language",
      "Select Language": "Select Language",
      "Conversation preferences": "Conversation preferences",
      "Voice settings": "Voice settings",
      "Camera permissions": "Camera permissions",
      "Data & Privacy": "Data & Privacy",
      "History": "History",
      "Notifications": "Notifications",
      "Export my data": "Export my data",
      "Help & Support": "Help & Support",
      "About Nadbrahma": "About Nadbrahma",
      "Dark mode": "Dark mode",
      "Optional observation": "Optional observation",
      "Log Out": "Log Out",
      "Welcome Back": "Welcome Back",
      "Email": "Email",
      "Password": "Password",
      "Log In": "Log In",
      "Create Account": "Create Account",
      "Display Name": "Display Name",
      "Continue Previous Session": "Continue Previous Session",
      "Daily reflection": "Daily reflection",
      "Explore Activities": "Explore Activities",
      "View History": "View History",
      "Your reflections are yours. You control what is saved and shared.": "Your reflections are yours. You control what is saved and shared."
    }
  },
  "hi": {
    "translation": {
      "Welcome to": "स्वागत है",
      "Nadbrahma": "नादब्रह्म",
      "A space to pause, reflect, and talk.": "रुकने, सोचने और बात करने की एक जगह।",
      "Get Started": "शुरू करें",
      "I already have an account": "मेरा पहले से एक अकाउंट है",
      "Good evening": "शुभ संध्या",
      "How are you feeling today?": "आज आप कैसा महसूस कर रहे हैं?",
      "Start a Session": "सत्र शुरू करें",
      "Profile": "प्रोफ़ाइल",
      "Language": "भाषा",
      "Select Language": "भाषा चुनें",
      "Conversation preferences": "वार्तालाप प्राथमिकताएँ",
      "Voice settings": "आवाज़ सेटिंग्स",
      "Camera permissions": "कैमरा अनुमतियाँ",
      "Data & Privacy": "डेटा और गोपनीयता",
      "History": "इतिहास",
      "Notifications": "सूचनाएं",
      "Export my data": "मेरा डेटा निर्यात करें",
      "Help & Support": "मदद और समर्थन",
      "About Nadbrahma": "नादब्रह्म के बारे में",
      "Dark mode": "डार्क मोड",
      "Optional observation": "वैकल्पिक अवलोकन",
      "Log Out": "लॉग आउट",
      "Welcome Back": "वापसी पर स्वागत है",
      "Email": "ईमेल",
      "Password": "पासवर्ड",
      "Log In": "लॉग इन",
      "Create Account": "खाता बनाएँ",
      "Display Name": "प्रदर्शन नाम",
      "Continue Previous Session": "पिछला सत्र जारी रखें",
      "Daily reflection": "दैनिक प्रतिबिंब",
      "Explore Activities": "गतिविधियां खोजें",
      "View History": "इतिहास देखें",
      "Your reflections are yours. You control what is saved and shared.": "आपके विचार आपके हैं। आप नियंत्रित करते हैं कि क्या सहेजा और साझा किया जाता है।"
    }
  },
  "mr": {
    "translation": {
      "Welcome to": "स्वागत आहे",
      "Nadbrahma": "नादब्रह्म",
      "A space to pause, reflect, and talk.": "थांबण्यासाठी, विचार करण्यासाठी आणि बोलण्यासाठी एक जागा.",
      "Get Started": "सुरू करा",
      "I already have an account": "माझे आधीच खाते आहे",
      "Good evening": "शुभ संध्याकाळ",
      "How are you feeling today?": "तुम्हाला आज कसे वाटत आहे?",
      "Start a Session": "सत्र सुरू करा",
      "Profile": "प्रोफाइल",
      "Language": "भाषा",
      "Select Language": "भाषा निवडा",
      "Conversation preferences": "संभाषण प्राधान्ये",
      "Voice settings": "आवाज सेटिंग्ज",
      "Camera permissions": "कॅमेरा परवानग्या",
      "Data & Privacy": "डेटा आणि गोपनीयता",
      "History": "इतिहास",
      "Notifications": "सूचना",
      "Export my data": "माझा डेटा निर्यात करा",
      "Help & Support": "मदत आणि समर्थन",
      "About Nadbrahma": "नादब्रह्म बद्दल",
      "Dark mode": "डार्क मोड",
      "Optional observation": "वैकल्पिक निरीक्षण",
      "Log Out": "लॉग आउट करा",
      "Welcome Back": "पुन्हा स्वागत आहे",
      "Email": "ईमेल",
      "Password": "पासवर्ड",
      "Log In": "लॉग इन करा",
      "Create Account": "खाते तयार करा",
      "Display Name": "प्रदर्शन नाव",
      "Continue Previous Session": "मागील सत्र सुरू ठेवा",
      "Daily reflection": "दैनिक प्रतिबिंब",
      "Explore Activities": "उपक्रम एक्सप्लोर करा",
      "View History": "इतिहास पहा",
      "Your reflections are yours. You control what is saved and shared.": "तुमचे विचार तुमचे आहेत. काय जतन केले आहे आणि सामायिक केले आहे ते तुम्ही नियंत्रित करता."
    }
  }
};

const LANGUAGE_KEY = '@app_language';

export const loadLanguage = async () => {
  try {
    const savedLang = await AsyncStorage.getItem(LANGUAGE_KEY);
    return savedLang || 'en';
  } catch (e) {
    return 'en';
  }
};

export const saveLanguage = async (lang: string) => {
  try {
    await AsyncStorage.setItem(LANGUAGE_KEY, lang);
    i18n.changeLanguage(lang);
  } catch (e) {}
};

i18n
  .use(initReactI18next)
  .init({
    compatibilityJSON: 'v3',
    resources,
    lng: 'en', // default, will be overridden on load
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

// Load the saved language immediately
loadLanguage().then(lang => {
  i18n.changeLanguage(lang);
});

export default i18n;

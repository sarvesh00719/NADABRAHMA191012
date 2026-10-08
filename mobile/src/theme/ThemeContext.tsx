import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const lightColors = {
  background: '#FAF7F2',
  surface: '#FFFFFF',
  primary: '#CA7C50',
  primaryLight: '#E8D2C4',
  text: '#1A202C',
  textSecondary: '#64748B',
  border: '#F1F5F9',
  error: '#EF4444'
};

export const darkColors = {
  background: '#0F172A',
  surface: '#1E293B',
  primary: '#CA7C50',
  primaryLight: '#334155',
  text: '#F8FAFC',
  textSecondary: '#94A3B8',
  border: '#334155',
  error: '#EF4444'
};

type ThemeContextType = {
  isDarkMode: boolean;
  setDarkMode: (value: boolean) => void;
  colors: typeof lightColors;
};

const ThemeContext = createContext<ThemeContextType>({
  isDarkMode: false,
  setDarkMode: () => {},
  colors: lightColors,
});

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem('@app_theme').then((savedTheme) => {
      if (savedTheme === 'dark') setIsDarkMode(true);
    });
  }, []);

  const setDarkMode = async (value: boolean) => {
    setIsDarkMode(value);
    await AsyncStorage.setItem('@app_theme', value ? 'dark' : 'light');
  };

  const colors = isDarkMode ? darkColors : lightColors;

  return (
    <ThemeContext.Provider value={{ isDarkMode, setDarkMode, colors }}>
      {children}
    </ThemeContext.Provider>
  );
};

import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useTranslation } from 'react-i18next';
import { useAuth } from "../../src/auth/AuthContext";
import { colors } from "../../src/theme/colors";

export default function Login() {
  const { login } = useAuth();
  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      await login({ email, password });
    } catch (e: any) {
      Alert.alert("Error", e.message || "Failed to login");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t("Welcome Back")}</Text>
      <TextInput style={styles.input} placeholder={t("Email")} value={email} onChangeText={setEmail} autoCapitalize="none" />
      <TextInput style={styles.input} placeholder={t("Password")} value={password} onChangeText={setPassword} secureTextEntry />
      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>{t("Log In")}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20, backgroundColor: colors.background },
  title: { fontSize: 28, fontWeight: "bold", color: colors.text, marginBottom: 30, textAlign: "center" },
  input: { backgroundColor: colors.surface, padding: 15, borderRadius: 8, marginBottom: 15, borderWidth: 1, borderColor: colors.border },
  button: { backgroundColor: colors.primary, padding: 15, borderRadius: 8, alignItems: "center" },
  buttonText: { color: colors.surface, fontWeight: "bold", fontSize: 16 }
});


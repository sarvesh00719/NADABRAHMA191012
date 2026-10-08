import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { useAuth } from "../../src/auth/AuthContext";
import { router } from "expo-router";
import { colors } from "../../src/theme/colors";

export default function Home() {
  const { user } = useAuth();
  return (
    <View style={styles.container}>
      <Text style={styles.greeting}>Hello, {user?.display_name || "Friend"}</Text>
      <Text style={styles.subtitle}>How are you feeling today?</Text>
      
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Daily Check-In</Text>
        <Text style={styles.cardText}>Take a moment to reflect on your energy and mood.</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.push("/session/setup")}>
          <Text style={styles.buttonText}>Start Check-In</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: colors.background, paddingTop: 60 },
  greeting: { fontSize: 28, fontWeight: "bold", color: colors.text },
  subtitle: { fontSize: 16, color: colors.textLight, marginBottom: 30 },
  card: { backgroundColor: colors.surface, padding: 20, borderRadius: 12, shadowColor: "#000", shadowOpacity: 0.1, shadowRadius: 5, elevation: 3 },
  cardTitle: { fontSize: 20, fontWeight: "bold", color: colors.text, marginBottom: 10 },
  cardText: { fontSize: 14, color: colors.textLight, marginBottom: 20 },
  button: { backgroundColor: colors.primary, padding: 15, borderRadius: 8, alignItems: "center" },
  buttonText: { color: colors.surface, fontWeight: "bold" }
});

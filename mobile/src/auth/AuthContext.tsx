import React, { createContext, useContext, useState, useEffect } from "react";
import * as SecureStore from "expo-secure-store";
import { fetchApi } from "../api/client";
import { User, AuthResponse } from "../api/types";
import { router } from "expo-router";

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (data: any) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkToken();
  }, []);

  async function checkToken() {
    try {
      const token = await SecureStore.getItemAsync("token");
      if (token) {
        const u = await fetchApi("/me");
        setUser(u);
      }
    } catch (e) {
      await SecureStore.deleteItemAsync("token");
    } finally {
      setIsLoading(false);
    }
  }

  const login = async (data: any) => {
    const res = await fetchApi("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
    await SecureStore.setItemAsync("token", res.access_token);
    setUser(res.user);
    if (!res.user.preferences?.onboarding_done) {
      router.replace("/(onboarding)/needs");
    } else {
      router.replace("/(tabs)/home");
    }
  };

  const register = async (data: any) => {
    const res = await fetchApi("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
    await SecureStore.setItemAsync("token", res.access_token);
    setUser(res.user);
    router.replace("/(onboarding)/needs");
  };

  const logout = async () => {
    await SecureStore.deleteItemAsync("token");
    setUser(null);
    router.replace("/(auth)/welcome");
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
};

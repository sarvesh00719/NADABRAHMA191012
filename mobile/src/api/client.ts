import * as SecureStore from 'expo-secure-store';
import { User, AuthResponse } from './types';

const API_URL = 'https://nadabrahma191012.onrender.com/api/v1';

export class ApiError extends Error {
  constructor(public code: string, message: string, public status: number) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const token = await SecureStore.getItemAsync('token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Bypass-Tunnel-Reminder': 'true',
    ...(options.headers as Record<string, string>),
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    if (response.status === 401) {
      await SecureStore.deleteItemAsync('token');
    }
    const data = await response.json().catch(() => ({}));
    throw new ApiError(
      data?.error?.code || 'UNKNOWN_ERROR',
      data?.error?.message || 'An error occurred',
      response.status
    );
  }

  if (response.status !== 204) {
    return response.json();
  }
}


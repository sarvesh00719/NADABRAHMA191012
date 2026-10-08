export interface UserPreferences {
  language: string;
  interaction_mode: string;
  needs: string[];
  retention: string;
  onboarding_done: boolean;
}

export interface User {
  id: string;
  email: string;
  display_name: string;
  locale: string;
  preferences?: UserPreferences;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface CheckIn {
  id: string;
  mood: string;
  energy: string;
  need: string;
  note?: string;
  created_at: string;
}

export interface CheckInList {
  items: CheckIn[];
  trend_available: boolean;
}

export interface SessionResponse {
  id: string;
  status: string;
  language: string;
  goal: string;
  started_at: string;
  opening_message?: { id: string; role: string; content: string };
}

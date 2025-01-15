export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  avatar?: string;
  specialization?: string;
  department?: string;
  status: UserStatus;
  lastActive?: Date;
  settings?: UserSettings;
}

export type UserRole = 'admin' | 'doctor' | 'nurse' | 'receptionist';

export type UserStatus = 'active' | 'inactive' | 'pending';

export interface UserSettings {
  notifications: boolean;
  theme: 'light' | 'dark';
  language: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

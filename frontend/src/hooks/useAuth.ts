import { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  department?: string;
  permissions: string[];
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    loading: true,
    error: null
  });

  const login = async (credentials: { email: string; password: string }) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      });

      if (!response.ok) throw new Error('فشل تسجيل الدخول');

      const data = await response.json();
      setAuthState({
        user: data.user,
        isAuthenticated: true,
        loading: false,
        error: null
      });

      localStorage.setItem('token', data.token);
    } catch (error) {
      setAuthState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'حدث خطأ غير معروف',
        loading: false
      }));
    }
  };

  const logout = async () => {
    try {
      await fetch('/api/auth/logout', {
        method: 'POST'
      });

      localStorage.removeItem('token');
      setAuthState({
        user: null,
        isAuthenticated: false,
        loading: false,
        error: null
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setAuthState(prev => ({ ...prev, loading: false }));
        return;
      }

      const response = await fetch('/api/auth/verify', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('جلسة غير صالحة');

      const data = await response.json();
      setAuthState({
        user: data.user,
        isAuthenticated: true,
        loading: false,
        error: null
      });
    } catch (error) {
      localStorage.removeItem('token');
      setAuthState({
        user: null,
        isAuthenticated: false,
        loading: false,
        error: error instanceof Error ? error.message : 'حدث خطأ في التحقق من الجلسة'
      });
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  return {
    user: authState.user,
    isAuthenticated: authState.isAuthenticated,
    loading: authState.loading,
    error: authState.error,
    login,
    logout,
    checkAuth
  };
};

export default useAuth;

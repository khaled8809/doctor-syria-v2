import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  User,
  AuthContextType,
  LoginCredentials,
  RegisterData,
  AuthState
} from '../types/auth';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    loading: true,
    error: null
  });
  const navigate = useNavigate();

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('/api/auth/me', {
            headers: { Authorization: `Bearer ${token}` }
          });
          setState({
            user: response.data,
            isAuthenticated: true,
            loading: false,
            error: null
          });
        } catch (error) {
          localStorage.removeItem('token');
          setState({
            user: null,
            isAuthenticated: false,
            loading: false,
            error: 'Session expired'
          });
        }
      } else {
        setState(prev => ({ ...prev, loading: false }));
      }
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const response = await axios.post('/api/auth/login', credentials);
      const { user, token } = response.data;
      localStorage.setItem('token', token);
      setState({
        user,
        isAuthenticated: true,
        loading: false,
        error: null
      });
      navigate('/dashboard');
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Login failed'
      }));
      throw error;
    }
  };

  const register = async (data: RegisterData) => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const response = await axios.post('/api/auth/register', data);
      const { user, token } = response.data;
      localStorage.setItem('token', token);
      setState({
        user,
        isAuthenticated: true,
        loading: false,
        error: null
      });
      navigate('/dashboard');
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Registration failed'
      }));
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setState({
      user: null,
      isAuthenticated: false,
      loading: false,
      error: null
    });
    navigate('/auth/login');
  };

  const resetPassword = async (email: string) => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      await axios.post('/api/auth/reset-password', { email });
      setState(prev => ({ ...prev, loading: false }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Password reset failed'
      }));
      throw error;
    }
  };

  const updateProfile = async (data: Partial<User>) => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const response = await axios.put('/api/auth/profile', data, {
        headers: getAuthHeaders()
      });
      setState(prev => ({
        ...prev,
        user: response.data,
        loading: false
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Profile update failed'
      }));
      throw error;
    }
  };

  const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return { Authorization: `Bearer ${token}` };
  };

  return (
    <AuthContext.Provider
      value={{
        ...state,
        login,
        register,
        logout,
        resetPassword,
        updateProfile,
        getAuthHeaders
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

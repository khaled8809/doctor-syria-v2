import { useState, useEffect } from 'react';
import { Settings, SettingsUpdate } from '../types/settings';

const DEFAULT_SETTINGS: Settings = {
  notifications: {
    email: true,
    push: true,
    sms: false,
  },
  privateProfile: false,
  dashboardView: 'grid',
  theme: 'light',
  language: 'en',
};

export const useSettings = () => {
  const [settings, setSettings] = useState<Settings>(() => {
    const savedSettings = localStorage.getItem('settings');
    return savedSettings ? JSON.parse(savedSettings) : DEFAULT_SETTINGS;
  });

  useEffect(() => {
    localStorage.setItem('settings', JSON.stringify(settings));
  }, [settings]);

  const updateSettings = (update: SettingsUpdate) => {
    setSettings((prev) => ({
      ...prev,
      ...update,
    }));
  };

  return { settings, updateSettings };
};

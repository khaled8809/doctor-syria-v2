import React, { createContext, useContext, useState, useEffect } from 'react';

interface Settings {
  themeMode: 'light' | 'dark';
  language: string;
  direction: 'ltr' | 'rtl';
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  dateFormat: string;
  timeFormat: '12h' | '24h';
}

interface SettingsContextType {
  settings: Settings;
  updateSettings: (newSettings: Partial<Settings>) => void;
  resetSettings: () => void;
}

const defaultSettings: Settings = {
  themeMode: 'light',
  language: 'ar',
  direction: 'rtl',
  notifications: {
    email: true,
    push: true,
    sms: false,
  },
  dateFormat: 'DD/MM/YYYY',
  timeFormat: '24h',
};

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

export const SettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [settings, setSettings] = useState<Settings>(() => {
    const storedSettings = localStorage.getItem('settings');
    return storedSettings ? JSON.parse(storedSettings) : defaultSettings;
  });

  useEffect(() => {
    localStorage.setItem('settings', JSON.stringify(settings));

    // Apply theme mode
    document.documentElement.setAttribute('data-theme', settings.themeMode);

    // Apply direction
    document.documentElement.setAttribute('dir', settings.direction);

    // Apply language
    document.documentElement.setAttribute('lang', settings.language);
  }, [settings]);

  const updateSettings = (newSettings: Partial<Settings>) => {
    setSettings((prevSettings) => ({
      ...prevSettings,
      ...newSettings,
    }));
  };

  const resetSettings = () => {
    setSettings(defaultSettings);
  };

  return (
    <SettingsContext.Provider
      value={{
        settings,
        updateSettings,
        resetSettings,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
};

export const useSettings = () => {
  const context = useContext(SettingsContext);
  if (context === undefined) {
    throw new Error('useSettings must be used within a SettingsProvider');
  }
  return context;
};

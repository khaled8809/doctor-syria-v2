export interface Settings {
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  privateProfile: boolean;
  dashboardView: string;
  theme: 'light' | 'dark';
  language: string;
}

export type NotificationSettings = {
  email: boolean;
  push: boolean;
  sms: boolean;
};

export type SettingsUpdate = Partial<Settings>;

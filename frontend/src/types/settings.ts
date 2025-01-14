export interface Settings {
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  theme: 'light' | 'dark';
  language: string;
  privateProfile: boolean;
  dashboardView: 'grid' | 'list';
}

export type SettingsUpdate = Partial<Settings>;

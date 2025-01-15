import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  FormControlLabel,
  FormGroup,
  Grid,
  Select,
  MenuItem,
  FormControl,
  SelectChangeEvent,
} from '@mui/material';
import { useSettings } from '../hooks/useSettings';
import { Settings as SettingsType } from '../types/settings';

const Settings: React.FC = () => {
  const { settings, updateSettings } = useSettings();
  const [localSettings, setLocalSettings] = useState<SettingsType>(settings);

  const handleNotificationChange = (type: keyof SettingsType['notifications']) => {
    const newSettings = {
      ...localSettings,
      notifications: {
        ...localSettings.notifications,
        [type]: !localSettings.notifications[type],
      },
    };
    setLocalSettings(newSettings);
    updateSettings({ notifications: newSettings.notifications });
  };

  const handlePrivateProfileChange = () => {
    const newSettings = {
      ...localSettings,
      privateProfile: !localSettings.privateProfile,
    };
    setLocalSettings(newSettings);
    updateSettings({ privateProfile: newSettings.privateProfile });
  };

  const handleThemeChange = (event: SelectChangeEvent<'light' | 'dark'>) => {
    const newSettings = {
      ...localSettings,
      theme: event.target.value as 'light' | 'dark',
    };
    setLocalSettings(newSettings);
    updateSettings({ theme: newSettings.theme });
  };

  const handleLanguageChange = (event: SelectChangeEvent<string>) => {
    const newSettings = {
      ...localSettings,
      language: event.target.value,
    };
    setLocalSettings(newSettings);
    updateSettings({ language: newSettings.language });
  };

  const handleDashboardViewChange = (event: SelectChangeEvent<string>) => {
    const newSettings = {
      ...localSettings,
      dashboardView: event.target.value,
    };
    setLocalSettings(newSettings);
    updateSettings({ dashboardView: newSettings.dashboardView });
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Notifications
              </Typography>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.notifications.email}
                      onChange={() => handleNotificationChange('email')}
                    />
                  }
                  label="Email Notifications"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.notifications.push}
                      onChange={() => handleNotificationChange('push')}
                    />
                  }
                  label="Push Notifications"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.notifications.sms}
                      onChange={() => handleNotificationChange('sms')}
                    />
                  }
                  label="SMS Notifications"
                />
              </FormGroup>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Privacy
              </Typography>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch
                      checked={localSettings.privateProfile}
                      onChange={handlePrivateProfileChange}
                    />
                  }
                  label="Private Profile"
                />
              </FormGroup>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Appearance
              </Typography>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <Select
                  value={localSettings.dashboardView}
                  onChange={handleDashboardViewChange}
                >
                  <MenuItem value="grid">Grid View</MenuItem>
                  <MenuItem value="list">List View</MenuItem>
                </Select>
              </FormControl>
              <FormControl fullWidth>
                <Select
                  value={localSettings.theme}
                  onChange={handleThemeChange}
                >
                  <MenuItem value="light">Light Theme</MenuItem>
                  <MenuItem value="dark">Dark Theme</MenuItem>
                </Select>
              </FormControl>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Language
              </Typography>
              <FormControl fullWidth>
                <Select
                  value={localSettings.language}
                  onChange={handleLanguageChange}
                >
                  <MenuItem value="en">English</MenuItem>
                  <MenuItem value="ar">Arabic</MenuItem>
                </Select>
              </FormControl>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;

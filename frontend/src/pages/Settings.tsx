import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
} from '@mui/material';
import {
  Brightness4,
  Notifications,
  Language,
  Lock,
  Visibility,
} from '@mui/icons-material';
import { useTheme } from '../hooks/useTheme';
import { useSettings } from '../contexts/SettingsContext';

const Settings: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const { settings, updateSettings } = useSettings();

  const handleLanguageChange = (event: SelectChangeEvent<string>) => {
    updateSettings({ language: event.target.value });
  };

  const handleNotificationsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    updateSettings({ notifications: event.target.checked });
  };

  const handlePrivacyChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    updateSettings({ privateProfile: event.target.checked });
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            الإعدادات
          </Typography>

          <List>
            <ListItem>
              <ListItemIcon>
                <Brightness4 />
              </ListItemIcon>
              <ListItemText
                primary="الوضع المظلم"
                secondary="تبديل بين الوضع الفاتح والمظلم"
              />
              <ListItemSecondaryAction>
                <Switch
                  edge="end"
                  checked={theme.palette.mode === 'dark'}
                  onChange={toggleTheme}
                />
              </ListItemSecondaryAction>
            </ListItem>

            <Divider />

            <ListItem>
              <ListItemIcon>
                <Language />
              </ListItemIcon>
              <ListItemText
                primary="اللغة"
                secondary="اختر لغة التطبيق"
              />
              <ListItemSecondaryAction>
                <FormControl variant="standard" sx={{ minWidth: 120 }}>
                  <Select
                    value={settings.language}
                    onChange={handleLanguageChange}
                  >
                    <MenuItem value="ar">العربية</MenuItem>
                    <MenuItem value="en">English</MenuItem>
                  </Select>
                </FormControl>
              </ListItemSecondaryAction>
            </ListItem>

            <Divider />

            <ListItem>
              <ListItemIcon>
                <Notifications />
              </ListItemIcon>
              <ListItemText
                primary="الإشعارات"
                secondary="تفعيل/تعطيل الإشعارات"
              />
              <ListItemSecondaryAction>
                <Switch
                  edge="end"
                  checked={settings.notifications}
                  onChange={handleNotificationsChange}
                />
              </ListItemSecondaryAction>
            </ListItem>

            <Divider />

            <ListItem>
              <ListItemIcon>
                <Lock />
              </ListItemIcon>
              <ListItemText
                primary="الخصوصية"
                secondary="جعل الملف الشخصي خاص"
              />
              <ListItemSecondaryAction>
                <Switch
                  edge="end"
                  checked={settings.privateProfile}
                  onChange={handlePrivacyChange}
                />
              </ListItemSecondaryAction>
            </ListItem>

            <Divider />

            <ListItem>
              <ListItemIcon>
                <Visibility />
              </ListItemIcon>
              <ListItemText
                primary="عرض لوحة التحكم"
                secondary="تخصيص عناصر لوحة التحكم"
              />
              <ListItemSecondaryAction>
                <FormControl variant="standard" sx={{ minWidth: 120 }}>
                  <Select
                    value={settings.dashboardView}
                    onChange={(e) => updateSettings({ dashboardView: e.target.value })}
                  >
                    <MenuItem value="compact">مضغوط</MenuItem>
                    <MenuItem value="comfortable">مريح</MenuItem>
                    <MenuItem value="spacious">واسع</MenuItem>
                  </Select>
                </FormControl>
              </ListItemSecondaryAction>
            </ListItem>
          </List>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Settings;

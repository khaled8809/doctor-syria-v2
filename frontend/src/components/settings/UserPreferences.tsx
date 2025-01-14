import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  FormControlLabel,
  Slider,
  Select,
  MenuItem,
  TextField,
  Button,
  Grid,
  Divider,
  IconButton,
  useTheme,
  Alert,
} from '@mui/material';
import {
  Palette,
  Notifications,
  Language,
  AccessibilityNew,
  Save,
  Refresh,
} from '@mui/icons-material';
import { useLocalStorage } from '../../hooks/useLocalStorage';
import { useNotificationService } from '../../services/notification-service';

interface UserPreferences {
  theme: {
    mode: 'light' | 'dark';
    primaryColor: string;
    fontSize: number;
    fontFamily: string;
    rtl: boolean;
  };
  notifications: {
    desktop: boolean;
    sound: boolean;
    email: boolean;
    priority: 'all' | 'high' | 'none';
  };
  diagnosis: {
    autoSave: boolean;
    confirmBeforeSave: boolean;
    showConfidence: boolean;
    riskThreshold: number;
  };
  language: {
    preferred: string;
    showTranslation: boolean;
    translateTo: string;
  };
  accessibility: {
    highContrast: boolean;
    largeText: boolean;
    reduceMotion: boolean;
    screenReader: boolean;
  };
}

const defaultPreferences: UserPreferences = {
  theme: {
    mode: 'light',
    primaryColor: '#1976d2',
    fontSize: 16,
    fontFamily: 'Tajawal',
    rtl: true,
  },
  notifications: {
    desktop: true,
    sound: true,
    email: false,
    priority: 'high',
  },
  diagnosis: {
    autoSave: true,
    confirmBeforeSave: true,
    showConfidence: true,
    riskThreshold: 0.7,
  },
  language: {
    preferred: 'ar',
    showTranslation: false,
    translateTo: 'en',
  },
  accessibility: {
    highContrast: false,
    largeText: false,
    reduceMotion: false,
    screenReader: false,
  },
};

const availableLanguages = [
  { code: 'ar', name: 'العربية' },
  { code: 'en', name: 'English' },
  { code: 'fr', name: 'Français' },
  { code: 'tr', name: 'Türkçe' },
];

const availableFonts = [
  'Tajawal',
  'Cairo',
  'Almarai',
  'IBM Plex Sans Arabic',
  'Noto Sans Arabic',
];

export default function UserPreferences() {
  const theme = useTheme();
  const [preferences, setPreferences] = useLocalStorage<UserPreferences>(
    'userPreferences',
    defaultPreferences
  );
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const { requestNotificationPermission } = useNotificationService();

  useEffect(() => {
    // تطبيق التفضيلات على مستوى التطبيق
    document.documentElement.style.fontSize = `${preferences.theme.fontSize}px`;
    document.documentElement.dir = preferences.theme.rtl ? 'rtl' : 'ltr';
    document.documentElement.lang = preferences.language.preferred;
  }, [preferences]);

  const handleThemeChange = (key: keyof UserPreferences['theme'], value: any) => {
    setPreferences((prev) => ({
      ...prev,
      theme: {
        ...prev.theme,
        [key]: value,
      },
    }));
  };

  const handleNotificationChange = async (key: keyof UserPreferences['notifications'], value: any) => {
    if (key === 'desktop' && value) {
      const granted = await requestNotificationPermission();
      if (!granted) {
        setMessage({
          type: 'error',
          text: 'لم يتم السماح بإشعارات سطح المكتب',
        });
        return;
      }
    }

    setPreferences((prev) => ({
      ...prev,
      notifications: {
        ...prev.notifications,
        [key]: value,
      },
    }));
  };

  const handleDiagnosisChange = (key: keyof UserPreferences['diagnosis'], value: any) => {
    setPreferences((prev) => ({
      ...prev,
      diagnosis: {
        ...prev.diagnosis,
        [key]: value,
      },
    }));
  };

  const handleLanguageChange = (key: keyof UserPreferences['language'], value: any) => {
    setPreferences((prev) => ({
      ...prev,
      language: {
        ...prev.language,
        [key]: value,
      },
    }));
  };

  const handleAccessibilityChange = (key: keyof UserPreferences['accessibility'], value: any) => {
    setPreferences((prev) => ({
      ...prev,
      accessibility: {
        ...prev.accessibility,
        [key]: value,
      },
    }));
  };

  const resetToDefaults = () => {
    setPreferences(defaultPreferences);
    setMessage({
      type: 'success',
      text: 'تم إعادة تعيين التفضيلات إلى الإعدادات الافتراضية',
    });
  };

  const savePreferences = () => {
    // يمكن إضافة المزيد من المنطق هنا مثل حفظ التفضيلات على الخادم
    setMessage({
      type: 'success',
      text: 'تم حفظ التفضيلات بنجاح',
    });
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h5">إعدادات المستخدم</Typography>
        <Box>
          <IconButton onClick={resetToDefaults} title="إعادة تعيين">
            <Refresh />
          </IconButton>
          <Button
            variant="contained"
            startIcon={<Save />}
            onClick={savePreferences}
            sx={{ ml: 1 }}
          >
            حفظ التغييرات
          </Button>
        </Box>
      </Box>

      {message && (
        <Alert
          severity={message.type}
          onClose={() => setMessage(null)}
          sx={{ mb: 3 }}
        >
          {message.text}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* المظهر */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Palette sx={{ mr: 1 }} />
                <Typography variant="h6">المظهر</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.theme.mode === 'dark'}
                    onChange={(e) => handleThemeChange('mode', e.target.checked ? 'dark' : 'light')}
                  />
                }
                label="الوضع الداكن"
              />

              <Box sx={{ mt: 2 }}>
                <Typography gutterBottom>حجم الخط</Typography>
                <Slider
                  value={preferences.theme.fontSize}
                  min={12}
                  max={24}
                  step={1}
                  marks
                  onChange={(_, value) => handleThemeChange('fontSize', value)}
                  valueLabelDisplay="auto"
                />
              </Box>

              <Box sx={{ mt: 2 }}>
                <Typography gutterBottom>نوع الخط</Typography>
                <Select
                  fullWidth
                  value={preferences.theme.fontFamily}
                  onChange={(e) => handleThemeChange('fontFamily', e.target.value)}
                >
                  {availableFonts.map((font) => (
                    <MenuItem key={font} value={font}>{font}</MenuItem>
                  ))}
                </Select>
              </Box>

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.theme.rtl}
                    onChange={(e) => handleThemeChange('rtl', e.target.checked)}
                  />
                }
                label="اتجاه من اليمين لليسار"
              />
            </CardContent>
          </Card>
        </Grid>

        {/* الإشعارات */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Notifications sx={{ mr: 1 }} />
                <Typography variant="h6">الإشعارات</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.notifications.desktop}
                    onChange={(e) => handleNotificationChange('desktop', e.target.checked)}
                  />
                }
                label="إشعارات سطح المكتب"
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.notifications.sound}
                    onChange={(e) => handleNotificationChange('sound', e.target.checked)}
                  />
                }
                label="الأصوات"
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.notifications.email}
                    onChange={(e) => handleNotificationChange('email', e.target.checked)}
                  />
                }
                label="إشعارات البريد الإلكتروني"
              />

              <Box sx={{ mt: 2 }}>
                <Typography gutterBottom>أولوية الإشعارات</Typography>
                <Select
                  fullWidth
                  value={preferences.notifications.priority}
                  onChange={(e) => handleNotificationChange('priority', e.target.value)}
                >
                  <MenuItem value="all">جميع الإشعارات</MenuItem>
                  <MenuItem value="high">الإشعارات المهمة فقط</MenuItem>
                  <MenuItem value="none">لا إشعارات</MenuItem>
                </Select>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* اللغة والترجمة */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Language sx={{ mr: 1 }} />
                <Typography variant="h6">اللغة والترجمة</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography gutterBottom>اللغة المفضلة</Typography>
                <Select
                  fullWidth
                  value={preferences.language.preferred}
                  onChange={(e) => handleLanguageChange('preferred', e.target.value)}
                >
                  {availableLanguages.map((lang) => (
                    <MenuItem key={lang.code} value={lang.code}>{lang.name}</MenuItem>
                  ))}
                </Select>
              </Box>

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.language.showTranslation}
                    onChange={(e) => handleLanguageChange('showTranslation', e.target.checked)}
                  />
                }
                label="عرض الترجمة"
              />

              {preferences.language.showTranslation && (
                <Box sx={{ mt: 2 }}>
                  <Typography gutterBottom>الترجمة إلى</Typography>
                  <Select
                    fullWidth
                    value={preferences.language.translateTo}
                    onChange={(e) => handleLanguageChange('translateTo', e.target.value)}
                  >
                    {availableLanguages
                      .filter((lang) => lang.code !== preferences.language.preferred)
                      .map((lang) => (
                        <MenuItem key={lang.code} value={lang.code}>{lang.name}</MenuItem>
                      ))}
                  </Select>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* إمكانية الوصول */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AccessibilityNew sx={{ mr: 1 }} />
                <Typography variant="h6">إمكانية الوصول</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.accessibility.highContrast}
                    onChange={(e) => handleAccessibilityChange('highContrast', e.target.checked)}
                  />
                }
                label="تباين عالي"
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.accessibility.largeText}
                    onChange={(e) => handleAccessibilityChange('largeText', e.target.checked)}
                  />
                }
                label="نص كبير"
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.accessibility.reduceMotion}
                    onChange={(e) => handleAccessibilityChange('reduceMotion', e.target.checked)}
                  />
                }
                label="تقليل الحركة"
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.accessibility.screenReader}
                    onChange={(e) => handleAccessibilityChange('screenReader', e.target.checked)}
                  />
                }
                label="دعم قارئ الشاشة"
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

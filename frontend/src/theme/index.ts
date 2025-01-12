import { createTheme, alpha } from '@mui/material/styles';
import { arEG } from '@mui/material/locale';

declare module '@mui/material/styles' {
  interface Palette {
    tertiary: Palette['primary'];
    neutral: Palette['primary'];
  }
  interface PaletteOptions {
    tertiary?: PaletteOptions['primary'];
    neutral?: PaletteOptions['primary'];
  }
}

const baseTheme = {
  direction: 'rtl',
  typography: {
    fontFamily: 'Tajawal, Arial, sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 700,
      lineHeight: 1.3,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h6: {
      fontSize: '1.125rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 500,
      lineHeight: 1.5,
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: 1.5,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 600,
      textTransform: 'none',
    },
  },
  shape: {
    borderRadius: 8,
  },
  spacing: 8,
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          padding: '8px 16px',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 12px 0 rgba(0,0,0,0.05)',
        },
      },
    },
    MuiCardContent: {
      styleOverrides: {
        root: {
          padding: 24,
          '&:last-child': {
            paddingBottom: 24,
          },
        },
      },
    },
    MuiTextField: {
      defaultProps: {
        variant: 'outlined',
        size: 'small',
      },
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          fontWeight: 500,
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: 12,
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
};

export const lightTheme = createTheme({
  ...baseTheme,
  palette: {
    mode: 'light',
    primary: {
      main: '#2563eb',
      light: '#60a5fa',
      dark: '#1d4ed8',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#7c3aed',
      light: '#a78bfa',
      dark: '#5b21b6',
      contrastText: '#ffffff',
    },
    tertiary: {
      main: '#059669',
      light: '#34d399',
      dark: '#047857',
      contrastText: '#ffffff',
    },
    neutral: {
      main: '#6b7280',
      light: '#9ca3af',
      dark: '#4b5563',
      contrastText: '#ffffff',
    },
    error: {
      main: '#dc2626',
      light: '#ef4444',
      dark: '#b91c1c',
    },
    warning: {
      main: '#d97706',
      light: '#f59e0b',
      dark: '#b45309',
    },
    info: {
      main: '#0284c7',
      light: '#0ea5e9',
      dark: '#0369a1',
    },
    success: {
      main: '#059669',
      light: '#10b981',
      dark: '#047857',
    },
    background: {
      default: '#f9fafb',
      paper: '#ffffff',
    },
    text: {
      primary: '#111827',
      secondary: '#4b5563',
      disabled: '#9ca3af',
    },
    divider: '#e5e7eb',
    action: {
      active: alpha('#111827', 0.54),
      hover: alpha('#111827', 0.04),
      selected: alpha('#111827', 0.08),
      disabled: alpha('#111827', 0.26),
      disabledBackground: alpha('#111827', 0.12),
    },
  },
}, arEG);

export const darkTheme = createTheme({
  ...baseTheme,
  palette: {
    mode: 'dark',
    primary: {
      main: '#60a5fa',
      light: '#93c5fd',
      dark: '#3b82f6',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#a78bfa',
      light: '#c4b5fd',
      dark: '#8b5cf6',
      contrastText: '#ffffff',
    },
    tertiary: {
      main: '#34d399',
      light: '#6ee7b7',
      dark: '#10b981',
      contrastText: '#ffffff',
    },
    neutral: {
      main: '#9ca3af',
      light: '#d1d5db',
      dark: '#6b7280',
      contrastText: '#ffffff',
    },
    error: {
      main: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
    },
    warning: {
      main: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
    },
    info: {
      main: '#0ea5e9',
      light: '#38bdf8',
      dark: '#0284c7',
    },
    success: {
      main: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    background: {
      default: '#111827',
      paper: '#1f2937',
    },
    text: {
      primary: '#f9fafb',
      secondary: '#d1d5db',
      disabled: '#6b7280',
    },
    divider: '#374151',
    action: {
      active: alpha('#f9fafb', 0.54),
      hover: alpha('#f9fafb', 0.04),
      selected: alpha('#f9fafb', 0.08),
      disabled: alpha('#f9fafb', 0.26),
      disabledBackground: alpha('#f9fafb', 0.12),
    },
  },
}, arEG);

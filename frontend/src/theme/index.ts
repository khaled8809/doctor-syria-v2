import { createTheme, Theme, ThemeOptions } from '@mui/material/styles';
import { PaletteOptions } from '@mui/material/styles/createPalette';

declare module '@mui/material/styles' {
  interface Palette {
    neutral: {
      main: string;
      contrastText: string;
    };
    tertiary: {
      main: string;
      light: string;
      dark: string;
      contrastText: string;
    };
  }

  interface PaletteOptions {
    neutral?: {
      main: string;
      contrastText: string;
    };
    tertiary?: {
      main: string;
      light: string;
      dark: string;
      contrastText: string;
    };
  }
}

const baseThemeOptions: ThemeOptions = {
  typography: {
    fontFamily: '"Inter", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      lineHeight: 1.2
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
      lineHeight: 1.4
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.57
    }
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          padding: '8px 16px',
          '&:hover': {
            boxShadow: 'none'
          }
        }
      }
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)'
        }
      }
    }
  }
};

const lightTheme = createTheme({
  ...baseThemeOptions,
  palette: {
    mode: 'light',
    primary: {
      main: '#0ea5e9',
      light: '#38bdf8',
      dark: '#0284c7',
      contrastText: '#ffffff'
    },
    secondary: {
      main: '#14b8a6',
      light: '#2dd4bf',
      dark: '#0f766e',
      contrastText: '#ffffff'
    },
    tertiary: {
      main: '#8b5cf6',
      light: '#a78bfa',
      dark: '#6d28d9',
      contrastText: '#ffffff'
    },
    error: {
      main: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
      contrastText: '#ffffff'
    },
    warning: {
      main: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
      contrastText: '#ffffff'
    },
    info: {
      main: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
      contrastText: '#ffffff'
    },
    success: {
      main: '#22c55e',
      light: '#4ade80',
      dark: '#16a34a',
      contrastText: '#ffffff'
    },
    grey: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827'
    },
    neutral: {
      main: '#64748b',
      contrastText: '#ffffff'
    },
    text: {
      primary: '#111827',
      secondary: '#4b5563',
      disabled: '#9ca3af'
    },
    divider: '#e5e7eb',
    background: {
      paper: '#ffffff',
      default: '#f9fafb'
    },
    action: {
      active: '#6b7280',
      hover: 'rgba(107, 114, 128, 0.04)',
      selected: 'rgba(107, 114, 128, 0.08)',
      disabled: 'rgba(107, 114, 128, 0.26)',
      disabledBackground: 'rgba(107, 114, 128, 0.12)',
      focus: 'rgba(107, 114, 128, 0.12)'
    }
  }
});

const darkTheme = createTheme({
  ...baseThemeOptions,
  palette: {
    mode: 'dark',
    primary: {
      main: '#0ea5e9',
      light: '#38bdf8',
      dark: '#0284c7',
      contrastText: '#ffffff'
    },
    secondary: {
      main: '#14b8a6',
      light: '#2dd4bf',
      dark: '#0f766e',
      contrastText: '#ffffff'
    },
    tertiary: {
      main: '#8b5cf6',
      light: '#a78bfa',
      dark: '#6d28d9',
      contrastText: '#ffffff'
    },
    error: {
      main: '#ef4444',
      light: '#f87171',
      dark: '#dc2626',
      contrastText: '#ffffff'
    },
    warning: {
      main: '#f59e0b',
      light: '#fbbf24',
      dark: '#d97706',
      contrastText: '#ffffff'
    },
    info: {
      main: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
      contrastText: '#ffffff'
    },
    success: {
      main: '#22c55e',
      light: '#4ade80',
      dark: '#16a34a',
      contrastText: '#ffffff'
    },
    grey: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827'
    },
    neutral: {
      main: '#64748b',
      contrastText: '#ffffff'
    },
    text: {
      primary: '#f9fafb',
      secondary: '#e5e7eb',
      disabled: '#9ca3af'
    },
    divider: '#374151',
    background: {
      paper: '#1f2937',
      default: '#111827'
    },
    action: {
      active: '#e5e7eb',
      hover: 'rgba(229, 231, 235, 0.04)',
      selected: 'rgba(229, 231, 235, 0.08)',
      disabled: 'rgba(229, 231, 235, 0.26)',
      disabledBackground: 'rgba(229, 231, 235, 0.12)',
      focus: 'rgba(229, 231, 235, 0.12)'
    }
  }
});

export { lightTheme, darkTheme };

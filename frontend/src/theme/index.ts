import { createTheme, PaletteColor, PaletteOptions, Theme } from '@mui/material';
import { TypographyOptions } from '@mui/material/styles/createTypography';

declare module '@mui/material/styles' {
  interface Palette {
    neutral: PaletteColor;
  }
  interface PaletteOptions {
    neutral?: PaletteColor;
  }
}

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2563eb',
      light: '#60a5fa',
      dark: '#1d4ed8',
      contrastText: '#ffffff'
    },
    secondary: {
      main: '#f43f5e',
      light: '#fb7185',
      dark: '#e11d48',
      contrastText: '#ffffff'
    },
    neutral: {
      main: '#64748b',
      light: '#94a3b8',
      dark: '#475569',
      contrastText: '#ffffff'
    },
    background: {
      default: '#f8fafc',
      paper: '#ffffff'
    }
  },
  typography: {
    fontFamily: 'Inter, system-ui, Avenir, Helvetica, Arial, sans-serif',
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
      fontWeight: 500,
      lineHeight: 1.4
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
      lineHeight: 1.4
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
      lineHeight: 1.4
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: 1.75
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: 1.57
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.57
    },
    button: {
      fontWeight: 600
    }
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 600,
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none'
          }
        },
        contained: {
          '&:hover': {
            boxShadow: 'none'
          }
        }
      }
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.05)'
        }
      }
    },
    MuiTextField: {
      defaultProps: {
        variant: 'outlined',
        size: 'small'
      },
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8
          }
        }
      }
    }
  }
});

export default theme;

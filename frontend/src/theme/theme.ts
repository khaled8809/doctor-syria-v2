import { createTheme, Theme, PaletteOptions, ThemeOptions } from '@mui/material/styles';
import { PaletteMode } from '@mui/material';
import { arEG } from '@mui/material/locale';

declare module '@mui/material/styles' {
  interface Palette {
    neutral: {
      main: string;
      contrastText: string;
    };
  }
  interface PaletteOptions {
    neutral?: {
      main: string;
      contrastText: string;
    };
  }
}

const getDesignTokens = (mode: PaletteMode): ThemeOptions => ({
  palette: {
    mode,
    primary: {
      main: '#2196F3',
      light: '#64B5F6',
      dark: '#1976D2'
    },
    secondary: {
      main: '#FF4081',
      light: '#FF80AB',
      dark: '#F50057'
    },
    neutral: {
      main: '#64748B',
      contrastText: '#fff'
    },
    background: {
      default: mode === 'light' ? '#F4F6F8' : '#121212',
      paper: mode === 'light' ? '#FFFFFF' : '#1E1E1E'
    }
  },
  direction: 'rtl',
  typography: {
    fontFamily: [
      'Cairo',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif'
    ].join(','),
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.43
    }
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarColor: '#6b6b6b #2b2b2b',
          '&::-webkit-scrollbar, & *::-webkit-scrollbar': {
            backgroundColor: mode === 'light' ? '#f5f5f5' : '#2b2b2b',
            width: 8,
          },
          '&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb': {
            borderRadius: 8,
            backgroundColor: mode === 'light' ? '#6b6b6b' : '#6b6b6b',
            minHeight: 24,
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)'
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

export const getTheme = (mode: PaletteMode): Theme => createTheme(getDesignTokens(mode), arEG);

const theme = getTheme('light');
export default theme;

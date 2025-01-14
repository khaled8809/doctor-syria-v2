import { useState, useMemo } from 'react';
import { createTheme, Theme } from '@mui/material/styles';
import { arEG } from '@mui/material/locale';

export const useTheme = () => {
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  const theme = useMemo<Theme>(
    () =>
      createTheme(
        {
          direction: 'rtl',
          palette: {
            mode,
            primary: {
              main: '#1976d2',
              light: '#42a5f5',
              dark: '#1565c0',
            },
            secondary: {
              main: '#9c27b0',
              light: '#ba68c8',
              dark: '#7b1fa2',
            },
            error: {
              main: '#d32f2f',
              light: '#ef5350',
              dark: '#c62828',
            },
            warning: {
              main: '#ed6c02',
              light: '#ff9800',
              dark: '#e65100',
            },
            info: {
              main: '#0288d1',
              light: '#03a9f4',
              dark: '#01579b',
            },
            success: {
              main: '#2e7d32',
              light: '#4caf50',
              dark: '#1b5e20',
            },
            background: {
              default: mode === 'light' ? '#f5f5f5' : '#121212',
              paper: mode === 'light' ? '#fff' : '#1e1e1e',
            },
          },
          typography: {
            fontFamily: 'Cairo, sans-serif',
            h1: {
              fontWeight: 700,
            },
            h2: {
              fontWeight: 600,
            },
            h3: {
              fontWeight: 600,
            },
            h4: {
              fontWeight: 600,
            },
            h5: {
              fontWeight: 500,
            },
            h6: {
              fontWeight: 500,
            },
          },
          components: {
            MuiButton: {
              styleOverrides: {
                root: {
                  fontWeight: 500,
                  textTransform: 'none',
                },
              },
            },
            MuiCard: {
              styleOverrides: {
                root: {
                  borderRadius: 8,
                },
              },
            },
            MuiPaper: {
              styleOverrides: {
                root: {
                  borderRadius: 8,
                },
              },
            },
          },
        },
        arEG
      ),
    [mode]
  );

  const toggleTheme = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  return { theme, toggleTheme };
};

export default useTheme;

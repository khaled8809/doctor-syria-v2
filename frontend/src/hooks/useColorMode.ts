import { useEffect } from 'react';
import { useLocalStorage } from './useLocalStorage';
import { PaletteMode } from '@mui/material';

export const useColorMode = () => {
  const [mode, setMode] = useLocalStorage<PaletteMode>('theme', 'light');

  const toggleColorMode = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', mode);
  }, [mode]);

  return {
    mode,
    toggleColorMode,
  };
};

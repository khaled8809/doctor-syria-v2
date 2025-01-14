import { Box, CircularProgress, useTheme } from '@mui/material';

const LoadingScreen = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        bgcolor: theme.palette.background.default,
      }}
    >
      <CircularProgress size={60} thickness={4} />
    </Box>
  );
};

export default LoadingScreen;

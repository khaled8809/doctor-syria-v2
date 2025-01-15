import { CircularProgress, Box } from '@mui/material';

interface LoadingOverlayProps {
  open?: boolean;
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ open = true }) => {
  if (!open) return null;

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.7)',
        zIndex: 9999,
      }}
    >
      <CircularProgress />
    </Box>
  );
};

export default LoadingOverlay;

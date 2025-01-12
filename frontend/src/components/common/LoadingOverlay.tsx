import React from 'react';
import {
  Box,
  CircularProgress,
  Typography,
  Backdrop,
  alpha,
  useTheme,
} from '@mui/material';

interface LoadingOverlayProps {
  open: boolean;
  message?: string;
  progress?: number;
  blur?: boolean;
}

export default function LoadingOverlay({
  open,
  message = 'جاري التحميل...',
  progress,
  blur = true,
}: LoadingOverlayProps) {
  const theme = useTheme();

  return (
    <Backdrop
      open={open}
      sx={{
        zIndex: theme.zIndex.drawer + 1,
        backgroundColor: blur
          ? alpha(theme.palette.background.paper, 0.7)
          : 'transparent',
        backdropFilter: blur ? 'blur(4px)' : 'none',
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          p: 3,
          borderRadius: 2,
          backgroundColor: alpha(theme.palette.background.paper, 0.9),
          boxShadow: theme.shadows[4],
        }}
      >
        <Box sx={{ position: 'relative', mb: 2 }}>
          <CircularProgress
            variant={progress !== undefined ? 'determinate' : 'indeterminate'}
            value={progress}
            size={48}
            thickness={4}
          />
          {progress !== undefined && (
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Typography
                variant="caption"
                component="div"
                sx={{ fontWeight: 600 }}
              >
                {Math.round(progress)}%
              </Typography>
            </Box>
          )}
        </Box>
        <Typography
          variant="body2"
          sx={{
            color: theme.palette.text.secondary,
            textAlign: 'center',
            maxWidth: 200,
          }}
        >
          {message}
        </Typography>
      </Box>
    </Backdrop>
  );
}

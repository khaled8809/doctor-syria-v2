import React from 'react';
import { Box, Typography, alpha, useTheme } from '@mui/material';

interface StatusBadgeProps {
  status: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  label: string;
  size?: 'small' | 'medium' | 'large';
  icon?: React.ReactNode;
}

export default function StatusBadge({
  status,
  label,
  size = 'medium',
  icon,
}: StatusBadgeProps) {
  const theme = useTheme();

  const getStatusColor = () => {
    switch (status) {
      case 'success':
        return theme.palette.success;
      case 'warning':
        return theme.palette.warning;
      case 'error':
        return theme.palette.error;
      case 'info':
        return theme.palette.info;
      default:
        return theme.palette.neutral;
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          py: 0.25,
          px: 1,
          fontSize: '0.75rem',
          iconSize: 16,
        };
      case 'large':
        return {
          py: 1,
          px: 2,
          fontSize: '1rem',
          iconSize: 24,
        };
      default:
        return {
          py: 0.5,
          px: 1.5,
          fontSize: '0.875rem',
          iconSize: 20,
        };
    }
  };

  const statusColor = getStatusColor();
  const sizeStyles = getSizeStyles();

  return (
    <Box
      sx={{
        display: 'inline-flex',
        alignItems: 'center',
        borderRadius: '999px',
        backgroundColor: alpha(statusColor.main, 0.1),
        border: `1px solid ${alpha(statusColor.main, 0.2)}`,
        color: statusColor.main,
        py: sizeStyles.py,
        px: sizeStyles.px,
        transition: 'all 0.2s ease-in-out',
        '&:hover': {
          backgroundColor: alpha(statusColor.main, 0.15),
        },
      }}
    >
      {icon && (
        <Box
          component="span"
          sx={{
            display: 'flex',
            mr: 0.5,
            '& > svg': {
              width: sizeStyles.iconSize,
              height: sizeStyles.iconSize,
            },
          }}
        >
          {icon}
        </Box>
      )}
      <Typography
        component="span"
        sx={{
          fontSize: sizeStyles.fontSize,
          fontWeight: 500,
          lineHeight: 1,
        }}
      >
        {label}
      </Typography>
    </Box>
  );
}

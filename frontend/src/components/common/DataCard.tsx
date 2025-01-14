import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  IconButton,
  Skeleton,
  useTheme,
  alpha,
  CardProps,
  Tooltip,
} from '@mui/material';
import { Info as InfoIcon } from '@mui/icons-material';

interface DataCardProps extends Omit<CardProps, 'children'> {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    label: string;
    positive?: boolean;
  };
  loading?: boolean;
  info?: string;
  color?: 'primary' | 'secondary' | 'tertiary' | 'neutral' | 'error' | 'warning' | 'info' | 'success';
}

export default function DataCard({
  title,
  value,
  subtitle,
  icon,
  trend,
  loading = false,
  info,
  color = 'primary',
  sx,
  ...props
}: DataCardProps) {
  const theme = useTheme();

  const getColorValue = (colorName: string) => {
    return theme.palette[colorName as keyof typeof theme.palette]?.main || theme.palette.primary.main;
  };

  const backgroundColor = alpha(getColorValue(color), 0.1);
  const textColor = getColorValue(color);

  if (loading) {
    return (
      <Card
        sx={{
          height: '100%',
          backgroundColor,
          ...sx,
        }}
        {...props}
      >
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Skeleton variant="text" width={120} />
            {info && <Skeleton variant="circular" width={24} height={24} sx={{ ml: 1 }} />}
          </Box>
          <Skeleton variant="rectangular" height={36} sx={{ mb: 1 }} />
          {subtitle && <Skeleton variant="text" width={80} />}
          {trend && <Skeleton variant="text" width={100} />}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card
      sx={{
        height: '100%',
        backgroundColor,
        transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: theme.shadows[4],
        },
        ...sx,
      }}
      {...props}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {icon && (
            <Box
              sx={{
                mr: 1,
                color: textColor,
              }}
            >
              {icon}
            </Box>
          )}
          <Typography
            variant="subtitle1"
            sx={{
              fontWeight: 500,
              color: theme.palette.text.secondary,
              flexGrow: 1,
            }}
          >
            {title}
          </Typography>
          {info && (
            <Tooltip title={info}>
              <IconButton size="small" sx={{ color: theme.palette.text.secondary }}>
                <InfoIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}
        </Box>

        <Typography
          variant="h4"
          sx={{
            mb: 1,
            color: textColor,
            fontWeight: 600,
          }}
        >
          {value}
        </Typography>

        {subtitle && (
          <Typography
            variant="body2"
            sx={{
              color: theme.palette.text.secondary,
              mb: trend ? 1 : 0,
            }}
          >
            {subtitle}
          </Typography>
        )}

        {trend && (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              color: trend.positive
                ? theme.palette.success.main
                : theme.palette.error.main,
            }}
          >
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              {trend.value}%
            </Typography>
            <Typography
              variant="caption"
              sx={{
                ml: 1,
                color: theme.palette.text.secondary,
              }}
            >
              {trend.label}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

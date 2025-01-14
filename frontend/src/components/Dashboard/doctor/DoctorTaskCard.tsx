import React from 'react';
import { Paper, Box, Typography } from '@mui/material';

interface DoctorTaskCardProps {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  color: string;
}

export const DoctorTaskCard: React.FC<DoctorTaskCardProps> = ({
  title,
  value,
  icon,
  color
}) => {
  return (
    <Paper
      sx={{
        p: 2,
        display: 'flex',
        flexDirection: 'column',
        height: 140,
        position: 'relative',
        overflow: 'hidden',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: 3,
          transition: 'all 0.3s'
        }
      }}
    >
      <Box
        sx={{
          position: 'absolute',
          top: -15,
          right: -15,
          backgroundColor: color,
          borderRadius: '50%',
          width: 80,
          height: 80,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          opacity: 0.2
        }}
      >
        {icon}
      </Box>

      <Typography variant="h6" component="div" gutterBottom>
        {title}
      </Typography>

      <Typography
        variant="h4"
        component="div"
        sx={{
          mt: 'auto',
          color: color,
          fontWeight: 'bold'
        }}
      >
        {value}
      </Typography>
    </Paper>
  );
};

export default DoctorTaskCard;

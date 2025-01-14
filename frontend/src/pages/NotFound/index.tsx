import React from 'react';
import { Box, Container, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const NotFound = () => {
  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          mt: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography variant="h1" component="h1" gutterBottom>
          404
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          الصفحة غير موجودة
        </Typography>
        <Button
          component={RouterLink}
          to="/"
          variant="contained"
          sx={{ mt: 3 }}
        >
          العودة إلى الصفحة الرئيسية
        </Button>
      </Box>
    </Container>
  );
};

export default NotFound;

import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const Prescriptions = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          الوصفات الطبية
        </Typography>
        {/* Add your prescriptions content here */}
      </Box>
    </Container>
  );
};

export default Prescriptions;

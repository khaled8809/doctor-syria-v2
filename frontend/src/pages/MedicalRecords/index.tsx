import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const MedicalRecords = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          السجلات الطبية
        </Typography>
        {/* Add your medical records content here */}
      </Box>
    </Container>
  );
};

export default MedicalRecords;

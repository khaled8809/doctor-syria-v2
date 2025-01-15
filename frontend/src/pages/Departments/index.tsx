import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const Departments = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          الأقسام
        </Typography>
        {/* Add your departments content here */}
      </Box>
    </Container>
  );
};

export default Departments;

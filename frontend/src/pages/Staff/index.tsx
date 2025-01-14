import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const Staff = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          الموظفون
        </Typography>
        {/* Add your staff content here */}
      </Box>
    </Container>
  );
};

export default Staff;

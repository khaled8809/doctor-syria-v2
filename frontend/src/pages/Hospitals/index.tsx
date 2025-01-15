import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const Hospitals = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          المستشفيات
        </Typography>
        {/* Add your hospitals content here */}
      </Box>
    </Container>
  );
};

export default Hospitals;

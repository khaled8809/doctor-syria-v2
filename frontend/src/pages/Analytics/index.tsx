import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const Analytics = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          التحليلات
        </Typography>
        {/* Add your analytics content here */}
      </Box>
    </Container>
  );
};

export default Analytics;

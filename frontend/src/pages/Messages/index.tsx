import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const Messages = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          الرسائل
        </Typography>
        {/* Add your messages content here */}
      </Box>
    </Container>
  );
};

export default Messages;

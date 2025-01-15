import React from 'react';
import { Box, Container, Typography, TextField, Button } from '@mui/material';

const ForgotPassword = () => {
  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5">
          نسيت كلمة المرور
        </Typography>
        <Box component="form" noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="البريد الإلكتروني"
            name="email"
            autoComplete="email"
            autoFocus
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            إرسال رابط إعادة تعيين كلمة المرور
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default ForgotPassword;

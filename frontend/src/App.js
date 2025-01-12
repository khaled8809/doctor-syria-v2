import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material';
import { BrowserRouter as Router } from 'react-router-dom';
import QuickSearch from './components/QuickSearch';
import ReviewsSection from './components/ReviewsSection';
import HealthBlog from './components/HealthBlog';

const theme = createTheme({
  direction: 'rtl',
  typography: {
    fontFamily: 'Tajawal, sans-serif',
  },
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <div className="App">
          <QuickSearch />
          <ReviewsSection />
          <HealthBlog />
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;

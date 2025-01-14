import React, { useEffect } from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { store } from './store';
import { lightTheme } from './theme';
import Layout from './components/Layout/Layout';
import { CssBaseline } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { SnackbarProvider } from 'notistack';
import Router from './router';

function App() {
  useEffect(() => {
    // Remove the server-side injected CSS
    const jssStyles = document.querySelector('#jss-server-side');
    if (jssStyles) {
      jssStyles.parentElement?.removeChild(jssStyles);
    }
  }, []);

  return (
    <Provider store={store}>
      <BrowserRouter basename="/doctor-syria-v2">
        <ThemeProvider theme={lightTheme}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <SnackbarProvider maxSnack={3}>
              <CssBaseline />
              <Layout>
                <Router />
              </Layout>
            </SnackbarProvider>
          </LocalizationProvider>
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  );
}

export default App;

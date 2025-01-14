import React, { useEffect } from 'react';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { SnackbarProvider } from 'notistack';
import { store } from './store';
import theme from './theme';
import Layout from './components/Layout/Layout';
import Router from './router';
import AppRoutes from './routes';
import { AuthProvider } from './contexts/AuthContext';
import { NotificationProvider } from './contexts/NotificationContext';
import { SettingsProvider } from './contexts/SettingsContext';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: false,
      staleTime: 30000
    }
  }
});

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
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <SnackbarProvider maxSnack={3}>
              <BrowserRouter basename="/doctor-syria-v2">
                <SettingsProvider>
                  <AuthProvider>
                    <NotificationProvider>
                      <CssBaseline />
                      <Layout>
                        <Router />
                      </Layout>
                    </NotificationProvider>
                  </AuthProvider>
                </SettingsProvider>
              </BrowserRouter>
            </SnackbarProvider>
          </LocalizationProvider>
        </ThemeProvider>
      </QueryClientProvider>
    </Provider>
  );
}

export default App;

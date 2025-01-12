import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  LocalHospital,
  AccessTime,
  MedicalServices,
  Healing,
  Language,
  Security
} from '@mui/icons-material';

const Home = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [stats, setStats] = useState({
    doctors: 0,
    hospitals: 0,
    patients: 0
  });

  useEffect(() => {
    // Fetch statistics from API
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    };
    fetchStats();
  }, []);

  const features = [
    {
      icon: <LocalHospital fontSize="large" />,
      title: t('features.hospitals'),
      description: t('features.hospitalsDesc')
    },
    {
      icon: <AccessTime fontSize="large" />,
      title: t('features.appointments'),
      description: t('features.appointmentsDesc')
    },
    {
      icon: <MedicalServices fontSize="large" />,
      title: t('features.services'),
      description: t('features.servicesDesc')
    },
    {
      icon: <Healing fontSize="large" />,
      title: t('features.treatment'),
      description: t('features.treatmentDesc')
    },
    {
      icon: <Language fontSize="large" />,
      title: t('features.language'),
      description: t('features.languageDesc')
    },
    {
      icon: <Security fontSize="large" />,
      title: t('features.security'),
      description: t('features.securityDesc')
    }
  ];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Hero Section */}
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'primary.contrastText',
          py: 8,
          mb: 6
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h2" component="h1" gutterBottom>
                {t('home.title')}
              </Typography>
              <Typography variant="h5" paragraph>
                {t('home.subtitle')}
              </Typography>
              <Button
                variant="contained"
                color="secondary"
                size="large"
                sx={{ mt: 2 }}
                href="/appointments"
              >
                {t('home.bookAppointment')}
              </Button>
            </Grid>
            <Grid item xs={12} md={6}>
              <img
                src="/images/hero-image.png"
                alt="Doctor Syria"
                style={{
                  width: '100%',
                  maxWidth: 500,
                  height: 'auto',
                  display: 'block',
                  margin: 'auto'
                }}
              />
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Statistics Section */}
      <Container maxWidth="lg" sx={{ mb: 6 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h3" color="primary">
                  {stats.doctors}+
                </Typography>
                <Typography variant="h6">{t('stats.doctors')}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h3" color="primary">
                  {stats.hospitals}+
                </Typography>
                <Typography variant="h6">{t('stats.hospitals')}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h3" color="primary">
                  {stats.patients}+
                </Typography>
                <Typography variant="h6">{t('stats.patients')}</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ mb: 6 }}>
        <Typography
          variant="h3"
          component="h2"
          align="center"
          gutterBottom
          sx={{ mb: 6 }}
        >
          {t('home.features')}
        </Typography>
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  p: 3
                }}
              >
                <Box sx={{ color: 'primary.main', mb: 2 }}>
                  {feature.icon}
                </Box>
                <Typography
                  variant="h5"
                  component="h3"
                  align="center"
                  gutterBottom
                >
                  {feature.title}
                </Typography>
                <Typography
                  variant="body1"
                  align="center"
                  color="text.secondary"
                >
                  {feature.description}
                </Typography>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box
        sx={{
          bgcolor: 'secondary.main',
          color: 'secondary.contrastText',
          py: 8
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h3" component="h2" gutterBottom>
                {t('home.ctaTitle')}
              </Typography>
              <Typography variant="h6" paragraph>
                {t('home.ctaDescription')}
              </Typography>
              <Button
                variant="contained"
                color="primary"
                size="large"
                href="/register"
              >
                {t('home.ctaButton')}
              </Button>
            </Grid>
            <Grid item xs={12} md={6}>
              <img
                src="/images/cta-image.png"
                alt="Join Us"
                style={{
                  width: '100%',
                  maxWidth: 400,
                  height: 'auto',
                  display: 'block',
                  margin: 'auto'
                }}
              />
            </Grid>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;

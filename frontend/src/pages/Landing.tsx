import React from 'react';
import { Box, Container, Typography, Button, Grid, Card, CardContent, useTheme, useMediaQuery } from '@mui/material';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';

// Custom styled components
const HeroSection = styled(Box)(({ theme }) => ({
  minHeight: '80vh',
  background: `linear-gradient(45deg, ${theme.palette.primary.main} 30%, ${theme.palette.secondary.main} 90%)`,
  display: 'flex',
  alignItems: 'center',
  color: theme.palette.common.white,
  position: 'relative',
  overflow: 'hidden',
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  height: '100%',
  transition: 'transform 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-10px)',
  },
}));

const StatsSection = styled(Box)(({ theme }) => ({
  padding: theme.spacing(8, 0),
  background: theme.palette.background.default,
}));

const Landing: React.FC = () => {
  const theme = useTheme();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const features = [
    {
      title: t('landing.features.appointments'),
      description: t('landing.features.appointmentsDesc'),
      icon: '🗓️',
    },
    {
      title: t('landing.features.records'),
      description: t('landing.features.recordsDesc'),
      icon: '📋',
    },
    {
      title: t('landing.features.pharmacy'),
      description: t('landing.features.pharmacyDesc'),
      icon: '💊',
    },
    {
      title: t('landing.features.laboratory'),
      description: t('landing.features.laboratoryDesc'),
      icon: '🔬',
    },
  ];

  const stats = [
    { number: '1000+', label: t('landing.stats.doctors') },
    { number: '50000+', label: t('landing.stats.patients') },
    { number: '100+', label: t('landing.stats.clinics') },
    { number: '24/7', label: t('landing.stats.support') },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <HeroSection>
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
              >
                <Typography variant="h2" component="h1" gutterBottom>
                  {t('landing.hero.title')}
                </Typography>
                <Typography variant="h5" paragraph>
                  {t('landing.hero.subtitle')}
                </Typography>
                <Box mt={4}>
                  <Button
                    variant="contained"
                    color="secondary"
                    size="large"
                    onClick={() => navigate('/register')}
                    sx={{ mr: 2 }}
                  >
                    {t('landing.hero.getStarted')}
                  </Button>
                  <Button
                    variant="outlined"
                    color="inherit"
                    size="large"
                    onClick={() => navigate('/contact')}
                  >
                    {t('landing.hero.contactUs')}
                  </Button>
                </Box>
              </motion.div>
            </Grid>
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8 }}
              >
                <img
                  src="/assets/images/hero-image.png"
                  alt="Doctor Syria"
                  style={{ width: '100%', maxWidth: '500px' }}
                />
              </motion.div>
            </Grid>
          </Grid>
        </Container>
      </HeroSection>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h3" align="center" gutterBottom>
          {t('landing.features.title')}
        </Typography>
        <Grid container spacing={4} sx={{ mt: 4 }}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <FeatureCard>
                  <CardContent>
                    <Typography variant="h1" align="center" gutterBottom>
                      {feature.icon}
                    </Typography>
                    <Typography variant="h6" align="center" gutterBottom>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" align="center" color="textSecondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </FeatureCard>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Stats Section */}
      <StatsSection>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            {stats.map((stat, index) => (
              <Grid item xs={6} md={3} key={index}>
                <motion.div
                  initial={{ opacity: 0 }}
                  whileInView={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <Typography variant="h3" align="center" color="primary">
                    {stat.number}
                  </Typography>
                  <Typography variant="subtitle1" align="center" color="textSecondary">
                    {stat.label}
                  </Typography>
                </motion.div>
              </Grid>
            ))}
          </Grid>
        </Container>
      </StatsSection>

      {/* CTA Section */}
      <Box sx={{ py: 8, textAlign: 'center' }}>
        <Container maxWidth="sm">
          <Typography variant="h4" gutterBottom>
            {t('landing.cta.title')}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary" paragraph>
            {t('landing.cta.subtitle')}
          </Typography>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/register')}
          >
            {t('landing.cta.button')}
          </Button>
        </Container>
      </Box>
    </Box>
  );
};

export default Landing;

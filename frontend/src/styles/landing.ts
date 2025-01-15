import { Theme } from '@mui/material/styles';

export const landingStyles = (theme: Theme) => ({
  root: {
    flexGrow: 1,
  },
  hero: {
    position: 'relative',
    color: theme.palette.common.white,
    minHeight: '80vh',
    display: 'flex',
    alignItems: 'center',
    background: `linear-gradient(45deg, ${theme.palette.primary.main} 30%, ${theme.palette.secondary.main} 90%)`,
    [theme.breakpoints.down('sm')]: {
      minHeight: '60vh',
    },
  },
  heroContent: {
    position: 'relative',
    zIndex: 1,
  },
  heroTitle: {
    fontWeight: 700,
    marginBottom: theme.spacing(4),
    [theme.breakpoints.down('sm')]: {
      fontSize: '2.5rem',
    },
  },
  heroSubtitle: {
    marginBottom: theme.spacing(4),
    [theme.breakpoints.down('sm')]: {
      fontSize: '1.2rem',
    },
  },
  heroButtons: {
    marginTop: theme.spacing(4),
  },
  featureCard: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    transition: 'transform 0.3s ease-in-out',
    '&:hover': {
      transform: 'translateY(-10px)',
    },
  },
  featureIcon: {
    fontSize: '3rem',
    marginBottom: theme.spacing(2),
    color: theme.palette.primary.main,
  },
  statsSection: {
    padding: theme.spacing(8, 0),
    backgroundColor: theme.palette.background.default,
  },
  statNumber: {
    fontWeight: 700,
    color: theme.palette.primary.main,
  },
  ctaSection: {
    padding: theme.spacing(8, 0),
    textAlign: 'center',
    backgroundColor: theme.palette.background.paper,
  },
  ctaTitle: {
    marginBottom: theme.spacing(2),
  },
  ctaSubtitle: {
    marginBottom: theme.spacing(4),
    color: theme.palette.text.secondary,
  },
  footer: {
    backgroundColor: theme.palette.primary.dark,
    color: theme.palette.common.white,
    padding: theme.spacing(6, 0),
  },
  socialIcon: {
    marginRight: theme.spacing(2),
    color: theme.palette.common.white,
    '&:hover': {
      color: theme.palette.secondary.main,
    },
  },
});

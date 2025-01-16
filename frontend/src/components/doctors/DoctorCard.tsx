import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Avatar,
  Chip,
  Rating,
  Grid,
  useTheme,
} from '@mui/material';
import { AccessTime, LocationOn, Phone, VideoCall } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Doctor } from '../../types/doctor';

interface DoctorCardProps {
  doctor: Doctor;
}

const DoctorCard: React.FC<DoctorCardProps> = ({ doctor }) => {
  const { t } = useTranslation();
  const theme = useTheme();
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card
        elevation={1}
        sx={{
          '&:hover': {
            boxShadow: theme.shadows[4],
            transform: 'translateY(-4px)',
            transition: 'all 0.3s ease-in-out',
          },
        }}
      >
        <CardContent>
          <Grid container spacing={3}>
            {/* صورة الطبيب */}
            <Grid item xs={12} sm={2}>
              <Box display="flex" justifyContent="center">
                <Avatar
                  src={doctor.image}
                  alt={doctor.name}
                  sx={{
                    width: 120,
                    height: 120,
                    border: `2px solid ${theme.palette.primary.main}`,
                  }}
                />
              </Box>
            </Grid>

            {/* معلومات الطبيب */}
            <Grid item xs={12} sm={7}>
              <Box>
                <Typography variant="h5" gutterBottom>
                  {doctor.title} {doctor.name}
                </Typography>
                
                <Typography color="textSecondary" gutterBottom>
                  {doctor.specialty}
                </Typography>

                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Rating value={doctor.rating} readOnly precision={0.5} />
                  <Typography variant="body2" color="textSecondary">
                    ({doctor.reviewsCount} {t('doctor.reviews')})
                  </Typography>
                </Box>

                <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
                  <Chip
                    icon={<LocationOn />}
                    label={doctor.area}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                  <Chip
                    icon={<AccessTime />}
                    label={t('doctor.experience', { years: doctor.experienceYears })}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                  {doctor.isAvailableOnline && (
                    <Chip
                      icon={<VideoCall />}
                      label={t('doctor.onlineConsultation')}
                      size="small"
                      color="success"
                    />
                  )}
                </Box>

                <Typography variant="body2" color="textSecondary">
                  {doctor.bio}
                </Typography>
              </Box>
            </Grid>

            {/* معلومات الحجز */}
            <Grid item xs={12} sm={3}>
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 2,
                  height: '100%',
                  justifyContent: 'center',
                  alignItems: 'flex-end',
                }}
              >
                <Typography variant="h6" color="primary">
                  {doctor.nextAvailable
                    ? t('doctor.nextAvailable', { date: doctor.nextAvailable })
                    : t('doctor.availableNow')}
                </Typography>

                <Typography variant="body2" color="textSecondary">
                  {t('doctor.consultationFee')}: {doctor.consultationFee}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>

        <CardActions sx={{ justifyContent: 'flex-end', p: 2 }}>
          <Button
            startIcon={<Phone />}
            variant="outlined"
            color="primary"
            onClick={() => navigate(`/doctors/${doctor.id}/contact`)}
          >
            {t('doctor.contact')}
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate(`/doctors/${doctor.id}/book`)}
          >
            {t('doctor.bookAppointment')}
          </Button>
        </CardActions>
      </Card>
    </motion.div>
  );
};

export default DoctorCard;

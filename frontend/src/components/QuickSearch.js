import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Autocomplete,
  Button,
  Grid,
  Typography,
  useTheme
} from '@mui/material';
import { Search, LocalHospital, MedicalServices } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const QuickSearch = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const [searchType, setSearchType] = useState('doctor');
  const [searchQuery, setSearchQuery] = useState('');
  const [location, setLocation] = useState(null);

  // مناطق سوريا الرئيسية
  const locations = [
    'دمشق',
    'حلب',
    'حمص',
    'حماة',
    'اللاذقية',
    'طرطوس',
    'دير الزور',
    'الحسكة',
    'الرقة',
    'درعا',
    'السويداء',
    'القنيطرة',
    'إدلب'
  ];

  // التخصصات الطبية
  const specialties = [
    'طب عام',
    'طب أطفال',
    'طب نساء وتوليد',
    'طب قلب',
    'طب عيون',
    'طب أسنان',
    'طب عظام',
    'طب نفسي',
    'طب جلدية',
    'طب باطني',
    'جراحة عامة',
    'جراحة عظام',
    'جراحة تجميل'
  ];

  const handleSearch = () => {
    // تنفيذ البحث وتوجيه المستخدم إلى صفحة النتائج
    const params = new URLSearchParams({
      type: searchType,
      query: searchQuery,
      location: location || ''
    });
    window.location.href = `/search?${params.toString()}`;
  };

  return (
    <Paper
      elevation={3}
      sx={{
        p: 3,
        mt: -5,
        mb: 6,
        mx: 'auto',
        maxWidth: 800,
        position: 'relative',
        zIndex: 2,
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)'
      }}
    >
      <Typography variant="h5" component="h2" gutterBottom align="center" color="primary">
        {t('search.title')}
      </Typography>
      
      <Grid container spacing={2} alignItems="center">
        {/* نوع البحث */}
        <Grid item xs={12} sm={3}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant={searchType === 'doctor' ? 'contained' : 'outlined'}
              onClick={() => setSearchType('doctor')}
              startIcon={<MedicalServices />}
              fullWidth
            >
              {t('search.doctors')}
            </Button>
            <Button
              variant={searchType === 'hospital' ? 'contained' : 'outlined'}
              onClick={() => setSearchType('hospital')}
              startIcon={<LocalHospital />}
              fullWidth
            >
              {t('search.hospitals')}
            </Button>
          </Box>
        </Grid>

        {/* حقل البحث */}
        <Grid item xs={12} sm={4}>
          <Autocomplete
            freeSolo
            options={specialties}
            value={searchQuery}
            onChange={(event, newValue) => setSearchQuery(newValue)}
            renderInput={(params) => (
              <TextField
                {...params}
                label={t('search.searchLabel')}
                variant="outlined"
                fullWidth
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            )}
          />
        </Grid>

        {/* اختيار المنطقة */}
        <Grid item xs={12} sm={3}>
          <Autocomplete
            options={locations}
            value={location}
            onChange={(event, newValue) => setLocation(newValue)}
            renderInput={(params) => (
              <TextField
                {...params}
                label={t('search.location')}
                variant="outlined"
                fullWidth
              />
            )}
          />
        </Grid>

        {/* زر البحث */}
        <Grid item xs={12} sm={2}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            size="large"
            startIcon={<Search />}
            onClick={handleSearch}
            sx={{ height: '56px' }}
          >
            {t('search.button')}
          </Button>
        </Grid>
      </Grid>

      {/* اقتراحات سريعة */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {t('search.popularSearches')}:
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {['طب أطفال', 'طب أسنان', 'طب نساء', 'طب عيون'].map((term) => (
            <Button
              key={term}
              variant="text"
              size="small"
              onClick={() => setSearchQuery(term)}
            >
              {term}
            </Button>
          ))}
        </Box>
      </Box>
    </Paper>
  );
};

export default QuickSearch;

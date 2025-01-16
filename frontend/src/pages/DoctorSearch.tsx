import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  TextField,
  Select,
  MenuItem,
  Button,
  Typography,
  Rating,
  Chip,
  Skeleton,
  useTheme,
  InputAdornment,
  IconButton,
} from '@mui/material';
import { Search, FilterList, LocationOn, AccessTime, Star } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { fetchDoctors, fetchSpecialties, fetchAreas } from '../services/api';
import DoctorCard from '../components/doctors/DoctorCard';
import SearchFilters from '../components/doctors/SearchFilters';
import ReviewsList from '../components/doctors/ReviewsList';
import BlogPreview from '../components/blog/BlogPreview';

const DoctorSearch: React.FC = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [searchParams, setSearchParams] = useSearchParams();
  const [showFilters, setShowFilters] = useState(!isMobile);

  // حالة البحث
  const [searchState, setSearchState] = useState({
    query: searchParams.get('q') || '',
    specialty: searchParams.get('specialty') || '',
    area: searchParams.get('area') || '',
    rating: searchParams.get('rating') ? Number(searchParams.get('rating')) : 0,
    availability: searchParams.get('availability') === 'true',
  });

  // استعلامات React Query
  const { data: doctors, isLoading: isLoadingDoctors } = useQuery(
    ['doctors', searchState],
    () => fetchDoctors(searchState)
  );

  const { data: specialties } = useQuery(['specialties'], fetchSpecialties);
  const { data: areas } = useQuery(['areas'], fetchAreas);

  // تحديث عنوان URL عند تغيير معايير البحث
  useEffect(() => {
    const params = new URLSearchParams();
    Object.entries(searchState).forEach(([key, value]) => {
      if (value) params.set(key, String(value));
    });
    setSearchParams(params);
  }, [searchState, setSearchParams]);

  const handleSearch = (newState: typeof searchState) => {
    setSearchState(newState);
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Grid container spacing={3}>
        {/* شريط البحث الرئيسي */}
        <Grid item xs={12}>
          <Card elevation={2}>
            <CardContent>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    placeholder={t('search.doctorPlaceholder')}
                    value={searchState.query}
                    onChange={(e) => handleSearch({ ...searchState, query: e.target.value })}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Search />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>
                <Grid item xs={12} md={4}>
                  <Select
                    fullWidth
                    value={searchState.specialty}
                    onChange={(e) => handleSearch({ ...searchState, specialty: e.target.value })}
                    displayEmpty
                  >
                    <MenuItem value="">{t('search.allSpecialties')}</MenuItem>
                    {specialties?.map((specialty) => (
                      <MenuItem key={specialty.id} value={specialty.id}>
                        {specialty.name}
                      </MenuItem>
                    ))}
                  </Select>
                </Grid>
                <Grid item xs={12} md={2}>
                  <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    startIcon={<FilterList />}
                    onClick={() => setShowFilters(!showFilters)}
                  >
                    {t('search.filters')}
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* الفلاتر والنتائج */}
        <Grid item xs={12}>
          <Grid container spacing={3}>
            {/* الفلاتر */}
            <AnimatePresence>
              {showFilters && (
                <Grid item xs={12} md={3}>
                  <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                  >
                    <SearchFilters
                      filters={searchState}
                      areas={areas || []}
                      onFilterChange={handleSearch}
                    />
                  </motion.div>
                </Grid>
              )}
            </AnimatePresence>

            {/* نتائج البحث */}
            <Grid item xs={12} md={showFilters ? 9 : 12}>
              {isLoadingDoctors ? (
                // حالة التحميل
                <Grid container spacing={2}>
                  {[1, 2, 3].map((n) => (
                    <Grid item xs={12} key={n}>
                      <Skeleton variant="rectangular" height={200} />
                    </Grid>
                  ))}
                </Grid>
              ) : doctors?.length ? (
                // عرض النتائج
                <Grid container spacing={2}>
                  {doctors.map((doctor) => (
                    <Grid item xs={12} key={doctor.id}>
                      <DoctorCard doctor={doctor} />
                    </Grid>
                  ))}
                </Grid>
              ) : (
                // لا توجد نتائج
                <Box
                  sx={{
                    textAlign: 'center',
                    py: 8,
                    color: 'text.secondary',
                  }}
                >
                  <Typography variant="h6">
                    {t('search.noResults')}
                  </Typography>
                </Box>
              )}
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
};

export default DoctorSearch;

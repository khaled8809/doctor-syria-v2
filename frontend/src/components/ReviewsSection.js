import React from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Avatar,
  Rating,
  Grid,
  useTheme
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { FormatQuote } from '@mui/icons-material';

const ReviewsSection = () => {
  const { t } = useTranslation();
  const theme = useTheme();

  const reviews = [
    {
      id: 1,
      name: 'أحمد محمد',
      avatar: '/avatars/user1.jpg',
      rating: 5,
      comment: 'خدمة ممتازة وسريعة. تمكنت من حجز موعد مع طبيب مختص في دقائق معدودة.',
      date: '2024-01-05',
      doctor: 'د. سمير حسن',
      specialty: 'طب قلب'
    },
    {
      id: 2,
      name: 'سارة خالد',
      avatar: '/avatars/user2.jpg',
      rating: 5,
      comment: 'المنصة سهلة الاستخدام وتوفر الكثير من الخيارات. أنصح بها بشدة.',
      date: '2024-01-03',
      doctor: 'د. ليلى عمر',
      specialty: 'طب أطفال'
    },
    {
      id: 3,
      name: 'محمد عبدالله',
      avatar: '/avatars/user3.jpg',
      rating: 4,
      comment: 'تجربة رائعة في حجز المواعيد ومتابعة العلاج. شكراً لفريق دكتور سوريا.',
      date: '2024-01-01',
      doctor: 'د. عمر خالد',
      specialty: 'طب عام'
    }
  ];

  return (
    <Box sx={{ py: 8, bgcolor: 'background.default' }}>
      <Container maxWidth="lg">
        <Typography
          variant="h3"
          component="h2"
          align="center"
          gutterBottom
          color="primary"
          sx={{ mb: 6 }}
        >
          {t('reviews.title')}
        </Typography>

        <Grid container spacing={4}>
          {reviews.map((review) => (
            <Grid item xs={12} md={4} key={review.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    transition: 'transform 0.3s ease-in-out'
                  }
                }}
              >
                <CardContent>
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 20,
                      right: 20,
                      color: theme.palette.primary.light,
                      opacity: 0.2
                    }}
                  >
                    <FormatQuote sx={{ fontSize: 60 }} />
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar
                      src={review.avatar}
                      alt={review.name}
                      sx={{ width: 60, height: 60, mr: 2 }}
                    />
                    <Box>
                      <Typography variant="h6" component="div">
                        {review.name}
                      </Typography>
                      <Rating value={review.rating} readOnly size="small" />
                    </Box>
                  </Box>

                  <Typography
                    variant="body1"
                    color="text.secondary"
                    paragraph
                    sx={{
                      minHeight: 80,
                      position: 'relative',
                      zIndex: 1
                    }}
                  >
                    {review.comment}
                  </Typography>

                  <Box
                    sx={{
                      mt: 2,
                      pt: 2,
                      borderTop: `1px solid ${theme.palette.divider}`,
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}
                  >
                    <Box>
                      <Typography variant="subtitle2" color="primary">
                        {review.doctor}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {review.specialty}
                      </Typography>
                    </Box>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(review.date).toLocaleDateString('ar-SY')}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default ReviewsSection;

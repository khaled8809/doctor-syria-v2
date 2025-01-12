import React from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CardMedia,
  Grid,
  Button,
  Chip,
  useTheme
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { AccessTime, ArrowBack } from '@mui/icons-material';

const HealthBlog = () => {
  const { t } = useTranslation();
  const theme = useTheme();

  const articles = [
    {
      id: 1,
      title: 'نصائح للوقاية من أمراض الشتاء',
      image: '/images/blog/winter-health.jpg',
      category: 'صحة عامة',
      date: '2024-01-10',
      readTime: '5 دقائق',
      excerpt: 'تعرف على أهم النصائح للحفاظ على صحتك خلال فصل الشتاء وتجنب الأمراض الموسمية.'
    },
    {
      id: 2,
      title: 'أحدث التقنيات في جراحة القلب',
      image: '/images/blog/heart-surgery.jpg',
      category: 'تقنيات طبية',
      date: '2024-01-08',
      readTime: '7 دقائق',
      excerpt: 'اكتشف أحدث التقنيات المستخدمة في جراحة القلب وكيف تحسن من نتائج العمليات.'
    },
    {
      id: 3,
      title: 'التغذية السليمة للأطفال',
      image: '/images/blog/kids-nutrition.jpg',
      category: 'تغذية',
      date: '2024-01-06',
      readTime: '6 دقائق',
      excerpt: 'دليلك الشامل للتغذية السليمة للأطفال وأهم العناصر الغذائية اللازمة لنموهم.'
    }
  ];

  return (
    <Box sx={{ py: 8, bgcolor: 'background.paper' }}>
      <Container maxWidth="lg">
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 6 }}>
          <Typography variant="h3" component="h2" color="primary">
            {t('blog.title')}
          </Typography>
          <Button
            variant="outlined"
            color="primary"
            endIcon={<ArrowBack />}
            href="/blog"
          >
            {t('blog.viewAll')}
          </Button>
        </Box>

        <Grid container spacing={4}>
          {articles.map((article) => (
            <Grid item xs={12} md={4} key={article.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    transition: 'transform 0.3s ease-in-out'
                  }
                }}
              >
                <CardMedia
                  component="img"
                  height="200"
                  image={article.image}
                  alt={article.title}
                  sx={{
                    objectFit: 'cover'
                  }}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ mb: 2 }}>
                    <Chip
                      label={article.category}
                      color="primary"
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Box
                      component="span"
                      sx={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        color: 'text.secondary',
                        typography: 'caption'
                      }}
                    >
                      <AccessTime sx={{ fontSize: 16, mr: 0.5 }} />
                      {article.readTime}
                    </Box>
                  </Box>

                  <Typography
                    gutterBottom
                    variant="h5"
                    component="h3"
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      minHeight: 64
                    }}
                  >
                    {article.title}
                  </Typography>

                  <Typography
                    color="text.secondary"
                    paragraph
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 3,
                      WebkitBoxOrient: 'vertical',
                      minHeight: 84
                    }}
                  >
                    {article.excerpt}
                  </Typography>

                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      mt: 2
                    }}
                  >
                    <Button
                      color="primary"
                      href={`/blog/${article.id}`}
                    >
                      {t('blog.readMore')}
                    </Button>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(article.date).toLocaleDateString('ar-SY')}
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

export default HealthBlog;

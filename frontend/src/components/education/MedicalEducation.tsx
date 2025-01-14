import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Button,
  Chip,
  Rating,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  TextField,
  InputAdornment,
  Tab,
  Tabs,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  LinearProgress,
} from '@mui/material';
import {
  Search as SearchIcon,
  PlayCircle as PlayCircleIcon,
  Book as BookIcon,
  School as SchoolIcon,
  Group as GroupIcon,
  VideoCall as VideoCallIcon,
  Bookmark as BookmarkIcon,
  BookmarkBorder as BookmarkBorderIcon,
  Share as ShareIcon,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

interface Course {
  id: string;
  title: string;
  description: string;
  instructor: {
    name: string;
    title: string;
    avatar: string;
  };
  thumbnail: string;
  duration: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  rating: number;
  reviews: number;
  enrolled: number;
  progress?: number;
  categories: string[];
}

interface Resource {
  id: string;
  title: string;
  type: 'article' | 'video' | 'document';
  author: string;
  date: string;
  thumbnail?: string;
  views: number;
  likes: number;
}

interface Webinar {
  id: string;
  title: string;
  speaker: string;
  date: string;
  time: string;
  thumbnail: string;
  attendees: number;
  isLive: boolean;
}

const MedicalEducation: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState(0);
  const [courses, setCourses] = useState<Course[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  const [webinars, setWebinars] = useState<Webinar[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [showWebinarDialog, setShowWebinarDialog] = useState(false);

  useEffect(() => {
    // Fetch educational content
    fetchEducationalContent();
  }, []);

  const fetchEducationalContent = async () => {
    // This would be replaced with actual API calls
    const mockCourses: Course[] = [
      {
        id: '1',
        title: 'أساسيات الطب الباطني',
        description: 'دورة شاملة في أساسيات الطب الباطني للأطباء المقيمين',
        instructor: {
          name: 'د. أحمد محمد',
          title: 'استشاري الطب الباطني',
          avatar: '/assets/images/doctors/doctor1.jpg',
        },
        thumbnail: '/assets/images/courses/internal-medicine.jpg',
        duration: '20 ساعة',
        level: 'intermediate',
        rating: 4.5,
        reviews: 128,
        enrolled: 450,
        progress: 35,
        categories: ['طب باطني', 'تعليم طبي'],
      },
    ];

    const mockResources: Resource[] = [
      {
        id: '1',
        title: 'التشخيص المبكر لأمراض القلب',
        type: 'article',
        author: 'د. سمير حسن',
        date: '2025-01-01',
        views: 1200,
        likes: 45,
      },
    ];

    const mockWebinars: Webinar[] = [
      {
        id: '1',
        title: 'المستجدات في علاج السكري',
        speaker: 'د. ليلى أحمد',
        date: '2025-01-15',
        time: '18:00',
        thumbnail: '/assets/images/webinars/diabetes.jpg',
        attendees: 120,
        isLive: false,
      },
    ];

    setCourses(mockCourses);
    setResources(mockResources);
    setWebinars(mockWebinars);
  };

  const renderCourses = () => (
    <Grid container spacing={3}>
      {courses.map(course => (
        <Grid item xs={12} sm={6} md={4} key={course.id}>
          <Card>
            <CardMedia
              component="img"
              height="200"
              image={course.thumbnail}
              alt={course.title}
            />
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {course.title}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Avatar
                  src={course.instructor.avatar}
                  sx={{ width: 24, height: 24, mr: 1 }}
                />
                <Typography variant="body2" color="textSecondary">
                  {course.instructor.name}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Rating value={course.rating} size="small" readOnly />
                <Typography variant="body2" color="textSecondary" sx={{ ml: 1 }}>
                  ({course.reviews})
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 1 }}>
                {course.categories.map(category => (
                  <Chip
                    key={category}
                    label={category}
                    size="small"
                    variant="outlined"
                  />
                ))}
              </Box>
              {course.progress !== undefined && (
                <Box sx={{ mt: 2 }}>
                  <LinearProgress
                    variant="determinate"
                    value={course.progress}
                    sx={{ mb: 1 }}
                  />
                  <Typography variant="body2" color="textSecondary">
                    {course.progress}% {t('education.completed')}
                  </Typography>
                </Box>
              )}
            </CardContent>
            <CardActions>
              <Button
                size="small"
                startIcon={<PlayCircleIcon />}
                onClick={() => setSelectedCourse(course)}
              >
                {course.progress !== undefined
                  ? t('education.continue')
                  : t('education.start')}
              </Button>
              <IconButton size="small">
                <BookmarkBorderIcon />
              </IconButton>
              <IconButton size="small">
                <ShareIcon />
              </IconButton>
            </CardActions>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  const renderResources = () => (
    <Grid container spacing={3}>
      {resources.map(resource => (
        <Grid item xs={12} sm={6} md={4} key={resource.id}>
          <Card>
            {resource.thumbnail && (
              <CardMedia
                component="img"
                height="140"
                image={resource.thumbnail}
                alt={resource.title}
              />
            )}
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {resource.title}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Chip
                  icon={
                    resource.type === 'article' ? (
                      <BookIcon />
                    ) : resource.type === 'video' ? (
                      <PlayCircleIcon />
                    ) : (
                      <SchoolIcon />
                    )
                  }
                  label={t(`education.resourceTypes.${resource.type}`)}
                  size="small"
                  sx={{ mr: 1 }}
                />
                <Typography variant="body2" color="textSecondary">
                  {resource.author}
                </Typography>
              </Box>
              <Typography variant="caption" color="textSecondary" display="block">
                {resource.date}
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small">
                {t('education.view')}
              </Button>
              <Box sx={{ flexGrow: 1 }} />
              <Typography variant="caption" color="textSecondary">
                {resource.views} {t('education.views')}
              </Typography>
            </CardActions>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  const renderWebinars = () => (
    <Grid container spacing={3}>
      {webinars.map(webinar => (
        <Grid item xs={12} sm={6} md={4} key={webinar.id}>
          <Card>
            <CardMedia
              component="img"
              height="140"
              image={webinar.thumbnail}
              alt={webinar.title}
            />
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {webinar.title}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <GroupIcon sx={{ mr: 1, color: 'text.secondary' }} />
                <Typography variant="body2" color="textSecondary">
                  {webinar.attendees} {t('education.attendees')}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                {webinar.isLive ? (
                  <Chip
                    label={t('education.live')}
                    color="error"
                    size="small"
                    sx={{ mr: 1 }}
                  />
                ) : (
                  <Typography variant="body2" color="textSecondary">
                    {webinar.date} {webinar.time}
                  </Typography>
                )}
              </Box>
            </CardContent>
            <CardActions>
              <Button
                size="small"
                startIcon={<VideoCallIcon />}
                onClick={() => setShowWebinarDialog(true)}
              >
                {webinar.isLive
                  ? t('education.joinNow')
                  : t('education.register')}
              </Button>
              <Box sx={{ flexGrow: 1 }} />
              <IconButton size="small">
                <ShareIcon />
              </IconButton>
            </CardActions>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          {t('education.title')}
        </Typography>

        {/* Search Bar */}
        <Paper sx={{ p: 2, mb: 3 }}>
          <TextField
            fullWidth
            placeholder={t('education.search')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Paper>

        {/* Navigation Tabs */}
        <Paper sx={{ mb: 3 }}>
          <Tabs
            value={activeTab}
            onChange={(_, newValue) => setActiveTab(newValue)}
            variant="scrollable"
            scrollButtons="auto"
          >
            <Tab
              icon={<SchoolIcon />}
              label={t('education.tabs.courses')}
            />
            <Tab
              icon={<BookIcon />}
              label={t('education.tabs.resources')}
            />
            <Tab
              icon={<VideoCallIcon />}
              label={t('education.tabs.webinars')}
            />
          </Tabs>
        </Paper>

        {/* Content */}
        <Box>
          {activeTab === 0 && renderCourses()}
          {activeTab === 1 && renderResources()}
          {activeTab === 2 && renderWebinars()}
        </Box>
      </Box>

      {/* Course Dialog */}
      <Dialog
        open={!!selectedCourse}
        onClose={() => setSelectedCourse(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedCourse?.title}
        </DialogTitle>
        <DialogContent>
          {/* Course content would go here */}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelectedCourse(null)}>
            {t('common.close')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Webinar Dialog */}
      <Dialog
        open={showWebinarDialog}
        onClose={() => setShowWebinarDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {t('education.webinar.register')}
        </DialogTitle>
        <DialogContent>
          {/* Registration form would go here */}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowWebinarDialog(false)}>
            {t('common.cancel')}
          </Button>
          <Button variant="contained" onClick={() => setShowWebinarDialog(false)}>
            {t('education.webinar.confirm')}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default MedicalEducation;

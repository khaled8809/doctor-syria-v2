import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Card,
  CardContent,
  CardMedia,
  Button,
  Chip,
} from '@mui/material';
import {
  Search as SearchIcon,
  ExpandMore as ExpandMoreIcon,
  Healing,
  Warning,
  CheckCircle,
  LocalHospital,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

interface FirstAidStep {
  id: number;
  title: string;
  description: string;
  image?: string;
  warning?: string;
}

interface FirstAidGuide {
  id: string;
  title: string;
  description: string;
  urgency: 'high' | 'medium' | 'low';
  steps: FirstAidStep[];
  warnings: string[];
  whenToSeekHelp: string[];
}

const FirstAidGuide: React.FC = () => {
  const { t } = useTranslation();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGuide, setSelectedGuide] = useState<FirstAidGuide | null>(null);

  const firstAidGuides: FirstAidGuide[] = [
    {
      id: 'burns',
      title: 'الحروق',
      description: 'إرشادات التعامل مع الحروق بمختلف درجاتها',
      urgency: 'high',
      steps: [
        {
          id: 1,
          title: 'إبعاد المصاب عن مصدر الحرق',
          description: 'قم بإبعاد المصاب عن مصدر الحرق فوراً لمنع المزيد من الضرر',
        },
        {
          id: 2,
          title: 'تبريد مكان الحرق',
          description: 'ضع المنطقة المصابة تحت ماء بارد جارٍ لمدة 10-20 دقيقة',
          warning: 'لا تستخدم الماء المثلج أو البارد جداً',
        },
      ],
      warnings: [
        'لا تضع مراهم أو زيوت على الحرق',
        'لا تفقع الفقاعات',
      ],
      whenToSeekHelp: [
        'إذا كان الحرق عميقاً',
        'إذا كانت المنطقة المصابة كبيرة',
        'إذا كان الحرق في الوجه أو المفاصل',
      ],
    },
    // يمكن إضافة المزيد من الإرشادات
  ];

  const filteredGuides = firstAidGuides.filter(guide =>
    guide.title.includes(searchQuery) ||
    guide.description.includes(searchQuery)
  );

  const renderUrgencyChip = (urgency: 'high' | 'medium' | 'low') => {
    const colors = {
      high: 'error',
      medium: 'warning',
      low: 'success',
    };

    return (
      <Chip
        label={t(`firstAid.urgency.${urgency}`)}
        color={colors[urgency] as any}
        size="small"
        sx={{ ml: 1 }}
      />
    );
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          {t('firstAid.title')}
        </Typography>

        <Alert severity="info" sx={{ mb: 3 }}>
          {t('firstAid.disclaimer')}
        </Alert>

        {/* Search Bar */}
        <Paper sx={{ p: 2, mb: 3 }}>
          <TextField
            fullWidth
            placeholder={t('firstAid.searchPlaceholder')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
            }}
          />
        </Paper>

        <Grid container spacing={3}>
          {/* First Aid Guides List */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                {t('firstAid.categories')}
              </Typography>
              <List>
                {filteredGuides.map(guide => (
                  <ListItem
                    button
                    key={guide.id}
                    onClick={() => setSelectedGuide(guide)}
                    selected={selectedGuide?.id === guide.id}
                  >
                    <ListItemIcon>
                      <Healing />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          {guide.title}
                          {renderUrgencyChip(guide.urgency)}
                        </Box>
                      }
                      secondary={guide.description}
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>

          {/* Selected Guide Details */}
          <Grid item xs={12} md={8}>
            {selectedGuide ? (
              <Paper sx={{ p: 2 }}>
                <Typography variant="h5" gutterBottom>
                  {selectedGuide.title}
                  {renderUrgencyChip(selectedGuide.urgency)}
                </Typography>

                <Typography variant="body1" sx={{ mb: 3 }}>
                  {selectedGuide.description}
                </Typography>

                {/* Steps */}
                <Typography variant="h6" gutterBottom>
                  {t('firstAid.steps')}
                </Typography>
                {selectedGuide.steps.map(step => (
                  <Card key={step.id} sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="h6" color="primary" gutterBottom>
                        {step.id}. {step.title}
                      </Typography>
                      <Typography variant="body1" paragraph>
                        {step.description}
                      </Typography>
                      {step.warning && (
                        <Alert severity="warning" sx={{ mt: 1 }}>
                          {step.warning}
                        </Alert>
                      )}
                      {step.image && (
                        <CardMedia
                          component="img"
                          height="200"
                          image={step.image}
                          alt={step.title}
                          sx={{ mt: 2, borderRadius: 1 }}
                        />
                      )}
                    </CardContent>
                  </Card>
                ))}

                {/* Warnings */}
                <Accordion sx={{ mb: 2 }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography color="error" sx={{ display: 'flex', alignItems: 'center' }}>
                      <Warning sx={{ mr: 1 }} />
                      {t('firstAid.warnings')}
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <List>
                      {selectedGuide.warnings.map((warning, index) => (
                        <ListItem key={index}>
                          <ListItemIcon>
                            <Warning color="error" />
                          </ListItemIcon>
                          <ListItemText primary={warning} />
                        </ListItem>
                      ))}
                    </List>
                  </AccordionDetails>
                </Accordion>

                {/* When to Seek Help */}
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography color="primary" sx={{ display: 'flex', alignItems: 'center' }}>
                      <LocalHospital sx={{ mr: 1 }} />
                      {t('firstAid.whenToSeekHelp')}
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <List>
                      {selectedGuide.whenToSeekHelp.map((condition, index) => (
                        <ListItem key={index}>
                          <ListItemIcon>
                            <CheckCircle color="primary" />
                          </ListItemIcon>
                          <ListItemText primary={condition} />
                        </ListItem>
                      ))}
                    </List>
                  </AccordionDetails>
                </Accordion>

                <Box sx={{ mt: 3, textAlign: 'center' }}>
                  <Button
                    variant="contained"
                    color="error"
                    size="large"
                    startIcon={<LocalHospital />}
                    onClick={() => {
                      // Navigate to emergency services
                    }}
                  >
                    {t('firstAid.emergencyServices')}
                  </Button>
                </Box>
              </Paper>
            ) : (
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Typography color="textSecondary">
                  {t('firstAid.selectGuide')}
                </Typography>
              </Paper>
            )}
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default FirstAidGuide;

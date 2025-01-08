import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  IconButton,
  Card,
  CardContent,
  LinearProgress,
  Alert,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from '@mui/lab';
import {
  Medication,
  LocalHospital,
  Assignment,
  Favorite,
  TrendingUp,
  Notifications,
} from '@mui/icons-material';
import { Line } from 'react-chartjs-2';
import { useTranslation } from 'react-i18next';

interface VitalSign {
  type: string;
  value: number;
  unit: string;
  timestamp: string;
  status: 'normal' | 'warning' | 'critical';
}

interface Medication {
  name: string;
  dosage: string;
  frequency: string;
  startDate: string;
  endDate: string;
  remainingDays: number;
}

const FollowUpDashboard: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState(0);
  const [vitalSigns, setVitalSigns] = useState<VitalSign[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch patient's follow-up data
    fetchFollowUpData();
  }, []);

  const fetchFollowUpData = async () => {
    try {
      // API calls will go here
      setLoading(false);
    } catch (error) {
      console.error('Error fetching follow-up data:', error);
      setLoading(false);
    }
  };

  const renderVitalSigns = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} md={8}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            {t('followUp.vitalSigns.chart')}
          </Typography>
          <Line
            data={{
              labels: ['1', '2', '3', '4', '5', '6', '7'],
              datasets: [
                {
                  label: t('followUp.vitalSigns.heartRate'),
                  data: [65, 70, 68, 72, 69, 71, 70],
                  borderColor: 'rgb(75, 192, 192)',
                  tension: 0.1,
                },
                {
                  label: t('followUp.vitalSigns.bloodPressure'),
                  data: [120, 118, 122, 119, 121, 120, 118],
                  borderColor: 'rgb(255, 99, 132)',
                  tension: 0.1,
                },
              ],
            }}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
              },
            }}
          />
        </Paper>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            {t('followUp.vitalSigns.current')}
          </Typography>
          <List>
            {vitalSigns.map((sign, index) => (
              <ListItem key={index}>
                <ListItemIcon>
                  <Favorite color={sign.status === 'normal' ? 'primary' : 'error'} />
                </ListItemIcon>
                <ListItemText
                  primary={sign.type}
                  secondary={`${sign.value} ${sign.unit}`}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Grid>
    </Grid>
  );

  const renderMedications = () => (
    <Grid container spacing={3}>
      {medications.map((med, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {med.name}
              </Typography>
              <Typography color="textSecondary">
                {med.dosage} - {med.frequency}
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" gutterBottom>
                  {t('followUp.medications.progress')}
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={(med.remainingDays / 30) * 100}
                  sx={{ mb: 1 }}
                />
                <Typography variant="caption">
                  {med.remainingDays} {t('followUp.medications.daysLeft')}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );

  const renderTimeline = () => (
    <Timeline position="alternate">
      <TimelineItem>
        <TimelineSeparator>
          <TimelineDot color="primary">
            <LocalHospital />
          </TimelineDot>
          <TimelineConnector />
        </TimelineSeparator>
        <TimelineContent>
          <Typography variant="h6" component="span">
            {t('followUp.timeline.appointment')}
          </Typography>
          <Typography>2025-01-15</Typography>
        </TimelineContent>
      </TimelineItem>
      {/* Add more timeline items */}
    </Timeline>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        {t('followUp.title')}
      </Typography>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        {t('followUp.nextAppointment')}: 2025-01-15
      </Alert>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
          <Tab label={t('followUp.tabs.vitalSigns')} />
          <Tab label={t('followUp.tabs.medications')} />
          <Tab label={t('followUp.tabs.timeline')} />
        </Tabs>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
          <LinearProgress />
        </Box>
      ) : (
        <Box sx={{ mt: 3 }}>
          {activeTab === 0 && renderVitalSigns()}
          {activeTab === 1 && renderMedications()}
          {activeTab === 2 && renderTimeline()}
        </Box>
      )}
    </Container>
  );
};

export default FollowUpDashboard;

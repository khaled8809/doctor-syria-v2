import React from 'react';
import { Grid, Paper, Typography, Box, Chip, Button } from '@mui/material';
import {
  AccessTime,
  Assignment,
  Favorite,
  NotificationsActive
} from '@mui/icons-material';
import { PatientVitalsList } from './PatientVitalsList';
import { TaskSchedule } from './TaskSchedule';
import { MedicationSchedule } from './MedicationSchedule';
import { useNurseStats } from '../../../hooks/useNurseStats';

const NurseDashboard: React.FC = () => {
  const { stats, tasks, patients, medications, loading } = useNurseStats();

  if (loading) return <div>جاري التحميل...</div>;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">لوحة تحكم الممرض</Typography>
        <Box>
          <Chip
            icon={<AccessTime />}
            label={`المناوبة: ${stats.currentShift}`}
            color="primary"
            sx={{ mr: 1 }}
          />
          <Button
            variant="contained"
            color="primary"
            startIcon={<NotificationsActive />}
          >
            تنبيه طارئ
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Current Ward Status */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              حالة الجناح الحالي
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">
                    {stats.totalPatients}
                  </Typography>
                  <Typography variant="body2">إجمالي المرضى</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="error">
                    {stats.criticalCases}
                  </Typography>
                  <Typography variant="body2">حالات حرجة</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="warning.main">
                    {stats.pendingTasks}
                  </Typography>
                  <Typography variant="body2">مهام معلقة</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="success.main">
                    {stats.completedTasks}
                  </Typography>
                  <Typography variant="body2">مهام مكتملة</Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              إجراءات سريعة
            </Typography>
            <Grid container spacing={1}>
              <Grid item xs={6}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Assignment />}
                  sx={{ mb: 1 }}
                >
                  تسجيل العلامات الحيوية
                </Button>
              </Grid>
              <Grid item xs={6}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Favorite />}
                  sx={{ mb: 1 }}
                >
                  طلب مساعدة طبيب
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Patient Vitals */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              العلامات الحيوية للمرضى
            </Typography>
            <PatientVitalsList patients={patients} />
          </Paper>
        </Grid>

        {/* Task Schedule */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              جدول المهام
            </Typography>
            <TaskSchedule tasks={tasks} />
          </Paper>
        </Grid>

        {/* Medication Schedule */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              جدول الأدوية
            </Typography>
            <MedicationSchedule medications={medications} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default NurseDashboard;

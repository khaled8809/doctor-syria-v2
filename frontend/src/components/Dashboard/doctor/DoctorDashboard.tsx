import React from 'react';
import { Grid, Paper, Typography, Box, Tabs, Tab, Button } from '@mui/material';
import {
  Schedule,
  Notifications,
  LocalHospital,
  Science
} from '@mui/icons-material';
import { AppointmentList } from './AppointmentList';
import { PatientsList } from './PatientsList';
import { LabResults } from './LabResults';
import { useDoctorStats } from '../../../hooks/useDoctorStats';
import { DoctorTaskCard } from './DoctorTaskCard';

interface DoctorStats {
  totalPatients: number;
  todayAppointments: number;
  pendingResults: number;
  completedDiagnoses: number;
  emergencyCases: number;
  activePatients: number;
  newLabResults: number;
}

interface DoctorAppointment {
  id: string;
  patientName: string;
  datetime: string;
  status: 'scheduled' | 'completed' | 'cancelled';
  type: string;
}

interface LabResult {
  id: string;
  patientName: string;
  testType: string;
  status: 'pending' | 'completed';
  date: string;
  results?: string;
}

const DoctorDashboard: React.FC = () => {
  const [tabValue, setTabValue] = React.useState(0);
  const { stats, appointments, patients, labResults, loading } = useDoctorStats<DoctorStats, DoctorAppointment[], LabResult[]>();

  if (loading) return <div>جاري التحميل...</div>;

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">لوحة تحكم الطبيب</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Schedule />}
        >
          إضافة موعد جديد
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Quick Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <DoctorTaskCard
            title="المواعيد اليوم"
            value={stats.todayAppointments}
            icon={<Schedule />}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DoctorTaskCard
            title="الحالات الطارئة"
            value={stats.emergencyCases}
            icon={<Notifications color="error" />}
            color="#d32f2f"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DoctorTaskCard
            title="المرضى تحت العلاج"
            value={stats.activePatients}
            icon={<LocalHospital />}
            color="#388e3c"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DoctorTaskCard
            title="نتائج مختبر جديدة"
            value={stats.newLabResults}
            icon={<Science />}
            color="#0288d1"
          />
        </Grid>

        {/* Main Content Tabs */}
        <Grid item xs={12}>
          <Paper sx={{ width: '100%' }}>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              indicatorColor="primary"
              textColor="primary"
              centered
            >
              <Tab label="المواعيد" />
              <Tab label="المرضى" />
              <Tab label="نتائج المختبر" />
            </Tabs>

            <Box sx={{ p: 3 }}>
              {tabValue === 0 && (
                <AppointmentList
                  appointments={appointments}
                  onAppointmentUpdate={(id, status) => {
                    // تحديث حالة الموعد
                  }}
                />
              )}
              {tabValue === 1 && (
                <PatientsList
                  patients={patients}
                  onPatientSelect={(id) => {
                    // فتح ملف المريض
                  }}
                />
              )}
              {tabValue === 2 && (
                <LabResults
                  results={labResults}
                  onResultReview={(id) => {
                    // مراجعة نتيجة المختبر
                  }}
                />
              )}
            </Box>
          </Paper>
        </Grid>

        {/* Communication Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              الرسائل والتنبيهات
            </Typography>
            {/* إضافة مكون الرسائل والتنبيهات */}
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              إجراءات سريعة
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6} md={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<LocalHospital />}
                >
                  كتابة وصفة طبية
                </Button>
              </Grid>
              <Grid item xs={6} md={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Science />}
                >
                  طلب تحليل
                </Button>
              </Grid>
              {/* إضافة المزيد من الإجراءات السريعة */}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DoctorDashboard;

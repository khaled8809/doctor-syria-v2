import { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  IconButton,
  useTheme,
} from '@mui/material';
import {
  People,
  EventAvailable,
  Notifications,
  TrendingUp,
  MoreVert,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';

// Dummy data for charts
const appointmentsData = [
  { month: 'يناير', appointments: 40 },
  { month: 'فبراير', appointments: 30 },
  { month: 'مارس', appointments: 45 },
  { month: 'أبريل', appointments: 50 },
  { month: 'مايو', appointments: 35 },
  { month: 'يونيو', appointments: 60 },
];

const patientsData = [
  { day: 'السبت', patients: 25 },
  { day: 'الأحد', patients: 32 },
  { day: 'الاثنين', patients: 28 },
  { day: 'الثلاثاء', patients: 35 },
  { day: 'الأربعاء', patients: 30 },
  { day: 'الخميس', patients: 40 },
  { day: 'الجمعة', patients: 20 },
];

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color }) => (
  <Card>
    <CardContent>
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Box>
          <Typography variant="subtitle2" color="text.secondary">
            {title}
          </Typography>
          <Typography variant="h4" sx={{ mt: 1, mb: 1 }}>
            {value}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            +10% من الشهر الماضي
          </Typography>
        </Box>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: 48,
            height: 48,
            borderRadius: 1,
            bgcolor: color + '22',
            color: color,
          }}
        >
          {icon}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const theme = useTheme();
  const [upcomingAppointments, setUpcomingAppointments] = useState([
    {
      id: 1,
      patientName: 'أحمد محمد',
      date: '2025-01-15',
      time: '10:00',
      type: 'كشف',
    },
    {
      id: 2,
      patientName: 'سارة أحمد',
      date: '2025-01-15',
      time: '11:30',
      type: 'متابعة',
    },
    {
      id: 3,
      patientName: 'محمد علي',
      date: '2025-01-15',
      time: '14:00',
      type: 'استشارة',
    },
  ]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 4 }}>
        لوحة المعلومات
      </Typography>

      <Grid container spacing={3}>
        {/* Stat Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="إجمالي المرضى"
            value="2,540"
            icon={<People />}
            color={theme.palette.primary.main}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="المواعيد اليوم"
            value="12"
            icon={<EventAvailable />}
            color={theme.palette.success.main}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="المواعيد هذا الشهر"
            value="156"
            icon={<TrendingUp />}
            color={theme.palette.warning.main}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="التنبيهات"
            value="5"
            icon={<Notifications />}
            color={theme.palette.error.main}
          />
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mb: 3,
              }}
            >
              <Typography variant="h6">إحصائيات المواعيد</Typography>
              <IconButton>
                <MoreVert />
              </IconButton>
            </Box>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={appointmentsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar
                  dataKey="appointments"
                  fill={theme.palette.primary.main}
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" sx={{ mb: 3 }}>
              المواعيد القادمة
            </Typography>
            {upcomingAppointments.map((appointment) => (
              <Box
                key={appointment.id}
                sx={{
                  p: 2,
                  mb: 2,
                  bgcolor: 'background.default',
                  borderRadius: 1,
                }}
              >
                <Typography variant="subtitle1">
                  {appointment.patientName}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {appointment.date} - {appointment.time}
                </Typography>
                <Typography
                  variant="caption"
                  sx={{
                    color: 'primary.main',
                    bgcolor: 'primary.lighter',
                    px: 1,
                    py: 0.5,
                    borderRadius: 1,
                  }}
                >
                  {appointment.type}
                </Typography>
              </Box>
            ))}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 3 }}>
              نشاط المرضى الأسبوعي
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={patientsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="patients"
                  stroke={theme.palette.primary.main}
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;

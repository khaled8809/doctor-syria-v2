import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  IconButton,
  LinearProgress,
  Tooltip,
} from '@mui/material';
import {
  People,
  LocalHospital,
  Assignment,
  TrendingUp,
  MoreVert,
  CalendarToday,
} from '@mui/icons-material';
import { useTheme } from '../hooks/useTheme';
import { useAuth } from '../hooks/useAuth';
import { useNotifications } from '../hooks/useNotifications';

const DashboardHome: React.FC = () => {
  const { theme } = useTheme();
  const { user } = useAuth();
  const { notifications } = useNotifications();

  const stats = {
    patients: {
      total: 150,
      active: 45,
      critical: 8,
    },
    appointments: {
      today: 25,
      completed: 15,
      pending: 10,
    },
    tasks: {
      total: 30,
      completed: 20,
      pending: 10,
    },
    resources: {
      utilization: 75,
      critical: 3,
      normal: 12,
    },
  };

  const StatCard = ({ title, value, icon, color }: any) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography color="textSecondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" component="div">
              {value}
            </Typography>
          </Box>
          <IconButton sx={{ backgroundColor: `${color}.light`, color: color }}>
            {icon}
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        مرحباً، {user?.name}
      </Typography>

      <Grid container spacing={3}>
        {/* إحصائيات سريعة */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="المرضى النشطين"
            value={stats.patients.active}
            icon={<People />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="المواعيد اليوم"
            value={stats.appointments.today}
            icon={<CalendarToday />}
            color="secondary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="المهام المعلقة"
            value={stats.tasks.pending}
            icon={<Assignment />}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="الحالات الحرجة"
            value={stats.patients.critical}
            icon={<LocalHospital />}
            color="error"
          />
        </Grid>

        {/* إحصائيات تفصيلية */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">استخدام الموارد</Typography>
                <IconButton size="small">
                  <MoreVert />
                </IconButton>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  نسبة الاستخدام الكلية
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Box sx={{ flexGrow: 1, mr: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={stats.resources.utilization}
                      sx={{ height: 8, borderRadius: 5 }}
                    />
                  </Box>
                  <Typography variant="body2" color="textSecondary">
                    {stats.resources.utilization}%
                  </Typography>
                </Box>
              </Box>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="error">
                    موارد حرجة: {stats.resources.critical}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="success">
                    موارد طبيعية: {stats.resources.normal}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">المواعيد اليوم</Typography>
                <IconButton size="small">
                  <MoreVert />
                </IconButton>
              </Box>
              <Grid container spacing={2}>
                <Grid item xs={4}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" color="primary">
                      {stats.appointments.today}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      الإجمالي
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={4}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" color="success">
                      {stats.appointments.completed}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      مكتمل
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={4}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h4" color="warning">
                      {stats.appointments.pending}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      معلق
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* إحصائيات المرضى */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">إحصائيات المرضى</Typography>
                <IconButton size="small">
                  <MoreVert />
                </IconButton>
              </Box>
              <Grid container spacing={3}>
                <Grid item xs={12} sm={4}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h3">{stats.patients.total}</Typography>
                    <Typography color="textSecondary">إجمالي المرضى</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h3">{stats.patients.active}</Typography>
                    <Typography color="textSecondary">المرضى النشطين</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h3" color="error">
                      {stats.patients.critical}
                    </Typography>
                    <Typography color="textSecondary">الحالات الحرجة</Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardHome;

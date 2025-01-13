import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import {
  TrendingUp,
  People,
  LocalHospital,
  AttachMoney
} from '@mui/icons-material';
import { KPICard } from '../common/KPICard';
import { LineChart } from '../charts/LineChart';
import { PieChart } from '../charts/PieChart';
import { useExecutiveStats } from '../../../hooks/useExecutiveStats';

const ExecutiveDashboard: React.FC = () => {
  const { stats, loading, error } = useExecutiveStats();

  if (loading) return <div>جاري التحميل...</div>;
  if (error) return <div>حدث خطأ في تحميل البيانات</div>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        لوحة تحكم المدير التنفيذي
      </Typography>

      <Grid container spacing={3}>
        {/* KPI Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="إجمالي المرضى"
            value={stats.totalPatients}
            icon={<People />}
            trend={stats.patientsTrend}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="الإيرادات"
            value={stats.revenue}
            icon={<AttachMoney />}
            trend={stats.revenueTrend}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="معدل الإشغال"
            value={stats.occupancyRate}
            icon={<LocalHospital />}
            trend={stats.occupancyTrend}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="معدل النمو"
            value={stats.growthRate}
            icon={<TrendingUp />}
            trend={stats.growthTrend}
          />
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              تحليل الإيرادات
            </Typography>
            <LineChart data={stats.revenueData} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              توزيع المرضى
            </Typography>
            <PieChart data={stats.patientDistribution} />
          </Paper>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              آخر النشاطات
            </Typography>
            {stats.recentActivities.map((activity) => (
              <Box key={activity.id} sx={{ mb: 1 }}>
                <Typography variant="body2">
                  {activity.description} - {activity.timestamp}
                </Typography>
              </Box>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ExecutiveDashboard;

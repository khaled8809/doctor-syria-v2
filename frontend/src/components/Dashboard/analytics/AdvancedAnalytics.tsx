import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Tooltip
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts';

interface AnalyticsProps {
  data: {
    patientMetrics: any[];
    departmentPerformance: any[];
    resourceUtilization: any[];
    financialMetrics: any[];
  };
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export const AdvancedAnalytics: React.FC<AnalyticsProps> = ({ data }) => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        التحليلات المتقدمة
      </Typography>

      <Grid container spacing={3}>
        {/* Patient Flow Analysis */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              تحليل تدفق المرضى
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.patientMetrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="admissions"
                  stroke="#8884d8"
                  name="حالات الدخول"
                />
                <Line
                  type="monotone"
                  dataKey="discharges"
                  stroke="#82ca9d"
                  name="حالات الخروج"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Department Performance */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              أداء الأقسام
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.departmentPerformance}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="department" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="efficiency" fill="#8884d8" name="الكفاءة" />
                <Bar dataKey="satisfaction" fill="#82ca9d" name="رضا المرضى" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Resource Utilization */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              استخدام الموارد
            </Typography>
            <Grid container spacing={2}>
              {data.resourceUtilization.map((resource) => (
                <Grid item xs={12} key={resource.name}>
                  <Box sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">{resource.name}</Typography>
                      <Typography variant="body2">{resource.usage}%</Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={resource.usage}
                      color={resource.usage > 80 ? 'error' : 'primary'}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Financial Metrics */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              المؤشرات المالية
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={data.financialMetrics}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {data.financialMetrics.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Predictive Analytics */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              التحليلات التنبؤية
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" color="primary">
                      التنبؤ بمعدل الإشغال
                    </Typography>
                    <Typography variant="h4" sx={{ mt: 2 }}>
                      85%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      متوقع خلال الأسبوع القادم
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" color="warning.main">
                      احتمالية نقص الموارد
                    </Typography>
                    <Typography variant="h4" sx={{ mt: 2 }}>
                      15%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      في قسم الطوارئ
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" color="success.main">
                      كفاءة العمليات
                    </Typography>
                    <Typography variant="h4" sx={{ mt: 2 }}>
                      92%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      معدل التحسن المتوقع
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AdvancedAnalytics;

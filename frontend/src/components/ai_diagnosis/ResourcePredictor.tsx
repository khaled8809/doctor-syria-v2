import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Alert,
  Stack,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';
import { DateRangePicker } from '@mui/x-date-pickers-pro/DateRangePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ar } from 'date-fns/locale';
import { useAIService } from '../../services/ai-service';
import { useTheme } from '@mui/material/styles';

interface ResourcePrediction {
  date: string;
  appointments: number;
  occupancy: number;
  waitingTime: number;
  resourceUtilization: {
    doctors: number;
    rooms: number;
    equipment: number;
  };
}

interface ResourceNeed {
  resource: string;
  current: number;
  predicted: number;
  shortage: boolean;
  recommendation: string;
}

export default function ResourcePredictor() {
  const theme = useTheme();
  const { predictAppointmentLoad, predictResourceNeeds } = useAIService();
  const [dateRange, setDateRange] = useState<[Date | null, Date | null]>([null, null]);
  const [timeframe, setTimeframe] = useState<string>('week');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [predictions, setPredictions] = useState<ResourcePrediction[]>([]);
  const [resourceNeeds, setResourceNeeds] = useState<ResourceNeed[]>([]);

  const loadPredictions = async () => {
    if (!dateRange[0] || !dateRange[1]) {
      setError('الرجاء اختيار نطاق زمني');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const [appointmentData, resourceData] = await Promise.all([
        predictAppointmentLoad({
          startDate: dateRange[0],
          endDate: dateRange[1],
        }),
        predictResourceNeeds(timeframe),
      ]);

      setPredictions(appointmentData);
      setResourceNeeds(resourceData);
    } catch (err) {
      setError('حدث خطأ في تحميل التنبؤات');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (dateRange[0] && dateRange[1]) {
      loadPredictions();
    }
  }, [dateRange, timeframe]);

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        التنبؤ بالمواعيد والموارد
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ar}>
                <DateRangePicker
                  localeText={{ start: 'من', end: 'إلى' }}
                  value={dateRange}
                  onChange={(newValue) => setDateRange(newValue)}
                />
              </LocalizationProvider>
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>الإطار الزمني</InputLabel>
                <Select
                  value={timeframe}
                  label="الإطار الزمني"
                  onChange={(e) => setTimeframe(e.target.value)}
                >
                  <MenuItem value="week">أسبوع</MenuItem>
                  <MenuItem value="month">شهر</MenuItem>
                  <MenuItem value="quarter">ربع سنة</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button
                variant="contained"
                fullWidth
                onClick={loadPredictions}
                disabled={loading}
              >
                تحديث
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {/* تنبؤات المواعيد */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>
                  تنبؤات المواعيد
                </Typography>
                <Box sx={{ height: 300 }}>
                  <ResponsiveContainer>
                    <LineChart
                      data={predictions}
                      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="appointments"
                        name="المواعيد"
                        stroke={theme.palette.primary.main}
                      />
                      <Line
                        type="monotone"
                        dataKey="occupancy"
                        name="نسبة الإشغال"
                        stroke={theme.palette.secondary.main}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* استخدام الموارد */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>
                  استخدام الموارد
                </Typography>
                <Box sx={{ height: 300 }}>
                  <ResponsiveContainer>
                    <AreaChart
                      data={predictions}
                      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Area
                        type="monotone"
                        dataKey="resourceUtilization.doctors"
                        name="الأطباء"
                        stackId="1"
                        fill={theme.palette.primary.light}
                      />
                      <Area
                        type="monotone"
                        dataKey="resourceUtilization.rooms"
                        name="الغرف"
                        stackId="1"
                        fill={theme.palette.secondary.light}
                      />
                      <Area
                        type="monotone"
                        dataKey="resourceUtilization.equipment"
                        name="المعدات"
                        stackId="1"
                        fill={theme.palette.error.light}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* احتياجات الموارد */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>
                  احتياجات الموارد المتوقعة
                </Typography>
                <Stack spacing={2}>
                  {resourceNeeds.map((need, index) => (
                    <Box
                      key={index}
                      sx={{
                        p: 2,
                        border: 1,
                        borderColor: 'divider',
                        borderRadius: 1,
                        bgcolor: need.shortage ? 'error.lighter' : 'success.lighter',
                      }}
                    >
                      <Typography variant="subtitle2" gutterBottom>
                        {need.resource}
                      </Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={6}>
                          <Typography variant="body2" color="text.secondary">
                            الحالي: {need.current}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body2" color="text.secondary">
                            المتوقع: {need.predicted}
                          </Typography>
                        </Grid>
                      </Grid>
                      {need.shortage && (
                        <Typography
                          variant="body2"
                          color="error"
                          sx={{ mt: 1 }}
                        >
                          {need.recommendation}
                        </Typography>
                      )}
                    </Box>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}

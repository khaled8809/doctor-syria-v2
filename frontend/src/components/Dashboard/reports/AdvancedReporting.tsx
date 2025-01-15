import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Button,
  TextField,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  PictureAsPdf,
  CloudDownload,
  Share,
  Print,
  FilterList,
  SaveAlt,
  Schedule
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

interface ReportConfig {
  type: string;
  dateRange: {
    start: Date;
    end: Date;
  };
  departments: string[];
  metrics: string[];
  format: 'pdf' | 'excel' | 'csv';
}

export const AdvancedReporting: React.FC = () => {
  const [reportConfig, setReportConfig] = useState<ReportConfig>({
    type: 'daily',
    dateRange: {
      start: new Date(),
      end: new Date(),
    },
    departments: [],
    metrics: [],
    format: 'pdf'
  });
  const [showFilters, setShowFilters] = useState(false);
  const [scheduledReports, setScheduledReports] = useState<any[]>([]);

  const reportTypes = [
    { value: 'daily', label: 'تقرير يومي' },
    { value: 'weekly', label: 'تقرير أسبوعي' },
    { value: 'monthly', label: 'تقرير شهري' },
    { value: 'custom', label: 'تقرير مخصص' }
  ];

  const departments = [
    { value: 'emergency', label: 'الطوارئ' },
    { value: 'surgery', label: 'الجراحة' },
    { value: 'pediatrics', label: 'الأطفال' },
    { value: 'cardiology', label: 'القلب' }
  ];

  const metrics = [
    { value: 'patients', label: 'عدد المرضى' },
    { value: 'occupancy', label: 'معدل الإشغال' },
    { value: 'revenue', label: 'الإيرادات' },
    { value: 'satisfaction', label: 'رضا المرضى' }
  ];

  const handleGenerateReport = () => {
    // توليد التقرير حسب الإعدادات المحددة
    console.log('Generating report with config:', reportConfig);
  };

  const handleScheduleReport = () => {
    // جدولة التقرير للإرسال التلقائي
    const newSchedule = {
      ...reportConfig,
      id: Math.random().toString(),
      frequency: 'daily',
      recipients: ['admin@hospital.com']
    };
    setScheduledReports([...scheduledReports, newSchedule]);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">نظام التقارير المتقدم</Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<FilterList />}
            onClick={() => setShowFilters(!showFilters)}
            sx={{ mr: 1 }}
          >
            الفلاتر
          </Button>
          <Button
            variant="outlined"
            startIcon={<Schedule />}
            onClick={handleScheduleReport}
            sx={{ mr: 1 }}
          >
            جدولة التقارير
          </Button>
          <Button
            variant="contained"
            startIcon={<PictureAsPdf />}
            onClick={handleGenerateReport}
          >
            إنشاء تقرير
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Report Configuration */}
        <Grid item xs={12} md={showFilters ? 8 : 12}>
          <Paper sx={{ p: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  select
                  label="نوع التقرير"
                  value={reportConfig.type}
                  onChange={(e) => setReportConfig({ ...reportConfig, type: e.target.value })}
                >
                  {reportTypes.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  select
                  label="تنسيق التقرير"
                  value={reportConfig.format}
                  onChange={(e) => setReportConfig({ ...reportConfig, format: e.target.value as any })}
                >
                  <MenuItem value="pdf">PDF</MenuItem>
                  <MenuItem value="excel">Excel</MenuItem>
                  <MenuItem value="csv">CSV</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12} md={6}>
                <DatePicker
                  label="من تاريخ"
                  value={reportConfig.dateRange.start}
                  onChange={(date) => setReportConfig({
                    ...reportConfig,
                    dateRange: { ...reportConfig.dateRange, start: date || new Date() }
                  })}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <DatePicker
                  label="إلى تاريخ"
                  value={reportConfig.dateRange.end}
                  onChange={(date) => setReportConfig({
                    ...reportConfig,
                    dateRange: { ...reportConfig.dateRange, end: date || new Date() }
                  })}
                />
              </Grid>
            </Grid>

            {/* Preview Table */}
            <TableContainer sx={{ mt: 3 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>القسم</TableCell>
                    <TableCell>عدد المرضى</TableCell>
                    <TableCell>معدل الإشغال</TableCell>
                    <TableCell>الإيرادات</TableCell>
                    <TableCell>رضا المرضى</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {departments.map((dept) => (
                    <TableRow key={dept.value}>
                      <TableCell>{dept.label}</TableCell>
                      <TableCell>120</TableCell>
                      <TableCell>85%</TableCell>
                      <TableCell>45,000</TableCell>
                      <TableCell>4.5/5</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            {/* Action Buttons */}
            <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
              <Button startIcon={<CloudDownload />}>
                تحميل
              </Button>
              <Button startIcon={<Share />}>
                مشاركة
              </Button>
              <Button startIcon={<Print />}>
                طباعة
              </Button>
              <Button startIcon={<SaveAlt />}>
                حفظ كقالب
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Filters Panel */}
        {showFilters && (
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                الفلاتر المتقدمة
              </Typography>
              <TextField
                fullWidth
                select
                label="الأقسام"
                SelectProps={{ multiple: true }}
                value={reportConfig.departments}
                onChange={(e) => setReportConfig({
                  ...reportConfig,
                  departments: e.target.value as string[]
                })}
                sx={{ mb: 2 }}
              >
                {departments.map((dept) => (
                  <MenuItem key={dept.value} value={dept.value}>
                    {dept.label}
                  </MenuItem>
                ))}
              </TextField>
              <TextField
                fullWidth
                select
                label="المقاييس"
                SelectProps={{ multiple: true }}
                value={reportConfig.metrics}
                onChange={(e) => setReportConfig({
                  ...reportConfig,
                  metrics: e.target.value as string[]
                })}
              >
                {metrics.map((metric) => (
                  <MenuItem key={metric.value} value={metric.value}>
                    {metric.label}
                  </MenuItem>
                ))}
              </TextField>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default AdvancedReporting;

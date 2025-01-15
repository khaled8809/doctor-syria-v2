import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  IconButton,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import {
  TrendingUp,
  PieChart,
  BarChart,
  Timeline,
  MoreVert,
  Download,
  Print,
  Share,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { arSA } from 'date-fns/locale';
import PDFDownloadButton from '../components/common/PDFDownloadButton';

const Reports: React.FC = () => {
  const [startDate, setStartDate] = useState<Date | null>(new Date());
  const [endDate, setEndDate] = useState<Date | null>(new Date());
  const [reportType, setReportType] = useState('daily');
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [openDialog, setOpenDialog] = useState(false);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleOpenDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleGenerateReport = () => {
    // Logic to generate report
    handleCloseDialog();
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">التقارير الطبية</Typography>
        <Box>
          <Button
            variant="contained"
            onClick={handleOpenDialog}
            sx={{ mr: 1 }}
          >
            إنشاء تقرير
          </Button>
          <IconButton onClick={handleClick}>
            <MoreVert />
          </IconButton>
        </Box>
      </Box>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem onClick={handleClose}>
          <Download sx={{ mr: 1 }} /> تحميل التقرير
        </MenuItem>
        <MenuItem onClick={handleClose}>
          <Print sx={{ mr: 1 }} /> طباعة
        </MenuItem>
        <MenuItem onClick={handleClose}>
          <Share sx={{ mr: 1 }} /> مشاركة
        </MenuItem>
      </Menu>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              الفلاتر
            </Typography>
            <Box sx={{ mt: 2 }}>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>نوع التقرير</InputLabel>
                <Select
                  value={reportType}
                  onChange={(e) => setReportType(e.target.value)}
                >
                  <MenuItem value="daily">يومي</MenuItem>
                  <MenuItem value="weekly">أسبوعي</MenuItem>
                  <MenuItem value="monthly">شهري</MenuItem>
                  <MenuItem value="yearly">سنوي</MenuItem>
                </Select>
              </FormControl>

              <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={arSA}>
                <DatePicker
                  label="من تاريخ"
                  value={startDate}
                  onChange={(newValue) => setStartDate(newValue)}
                  sx={{ width: '100%', mb: 2 }}
                />
                <DatePicker
                  label="إلى تاريخ"
                  value={endDate}
                  onChange={(newValue) => setEndDate(newValue)}
                  sx={{ width: '100%', mb: 2 }}
                />
              </LocalizationProvider>

              <Button variant="contained" fullWidth>
                تطبيق الفلتر
              </Button>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={9}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    إجمالي المرضى
                  </Typography>
                  <Typography variant="h4">1,234</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingUp color="success" />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      +15% من الشهر الماضي
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    المواعيد
                  </Typography>
                  <Typography variant="h4">856</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingUp color="success" />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      +8% من الشهر الماضي
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    العمليات
                  </Typography>
                  <Typography variant="h4">145</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingUp color="success" />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      +12% من الشهر الماضي
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    الإيرادات
                  </Typography>
                  <Typography variant="h4">$52K</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingUp color="success" />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      +18% من الشهر الماضي
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    توزيع المرضى حسب القسم
                  </Typography>
                  {/* Add Chart Component Here */}
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    توزيع المواعيد
                  </Typography>
                  {/* Add Chart Component Here */}
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    الإيرادات الشهرية
                  </Typography>
                  {/* Add Chart Component Here */}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>
      </Grid>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>إنشاء تقرير جديد</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>نوع التقرير</InputLabel>
              <Select value={reportType} onChange={(e) => setReportType(e.target.value)}>
                <MenuItem value="patient">تقرير المرضى</MenuItem>
                <MenuItem value="appointment">تقرير المواعيد</MenuItem>
                <MenuItem value="revenue">تقرير الإيرادات</MenuItem>
                <MenuItem value="department">تقرير الأقسام</MenuItem>
              </Select>
            </FormControl>

            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={arSA}>
              <DatePicker
                label="من تاريخ"
                value={startDate}
                onChange={(newValue) => setStartDate(newValue)}
                sx={{ width: '100%', mb: 2 }}
              />
              <DatePicker
                label="إلى تاريخ"
                value={endDate}
                onChange={(newValue) => setEndDate(newValue)}
                sx={{ width: '100%', mb: 2 }}
              />
            </LocalizationProvider>

            <TextField
              fullWidth
              multiline
              rows={4}
              label="ملاحظات"
              variant="outlined"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>إلغاء</Button>
          <Button onClick={handleGenerateReport} variant="contained">
            إنشاء التقرير
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Reports;

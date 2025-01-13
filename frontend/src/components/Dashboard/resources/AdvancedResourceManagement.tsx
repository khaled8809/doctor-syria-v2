import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  IconButton,
  Button,
  Chip,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Tooltip
} from '@mui/material';
import {
  Inventory,
  TrendingUp,
  Warning,
  Add,
  Edit,
  Delete,
  Refresh,
  Timeline,
  Assessment
} from '@mui/icons-material';

interface Resource {
  id: string;
  name: string;
  category: string;
  quantity: number;
  minThreshold: number;
  maxThreshold: number;
  unit: string;
  location: string;
  status: 'available' | 'low' | 'critical' | 'excess';
  lastUpdated: Date;
  cost: number;
  supplier: string;
}

interface ResourcePrediction {
  resourceId: string;
  predictedDemand: number;
  confidence: number;
  trend: 'increasing' | 'decreasing' | 'stable';
  recommendations: string[];
}

export const AdvancedResourceManagement: React.FC = () => {
  const [resources, setResources] = useState<Resource[]>([]);
  const [predictions, setPredictions] = useState<ResourcePrediction[]>([]);
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);
  const [addResourceDialog, setAddResourceDialog] = useState(false);
  const [resourceMetrics, setResourceMetrics] = useState({
    totalValue: 0,
    utilizationRate: 0,
    criticalItems: 0,
    efficiency: 0
  });

  useEffect(() => {
    // تحميل البيانات الأولية
    fetchResourceData();
  }, []);

  const fetchResourceData = async () => {
    // API calls to fetch resources and predictions
  };

  const calculateResourceStatus = (resource: Resource): string => {
    const ratio = resource.quantity / resource.minThreshold;
    if (ratio < 0.5) return 'critical';
    if (ratio < 1) return 'low';
    if (resource.quantity > resource.maxThreshold) return 'excess';
    return 'available';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'critical':
        return 'error';
      case 'low':
        return 'warning';
      case 'excess':
        return 'info';
      default:
        return 'success';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">إدارة الموارد المتقدمة</Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<Assessment />}
            sx={{ mr: 1 }}
          >
            التقارير
          </Button>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setAddResourceDialog(true)}
          >
            إضافة مورد
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Resource Metrics */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                القيمة الإجمالية
              </Typography>
              <Typography variant="h4">
                ${resourceMetrics.totalValue.toLocaleString()}
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={resourceMetrics.utilizationRate}
                sx={{ mt: 2 }}
              />
              <Typography variant="caption" color="text.secondary">
                معدل الاستخدام: {resourceMetrics.utilizationRate}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                العناصر الحرجة
              </Typography>
              <Typography variant="h4" color="error">
                {resourceMetrics.criticalItems}
              </Typography>
              <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                <Warning color="error" />
                <Typography variant="body2" sx={{ ml: 1 }}>
                  تحتاج إلى اهتمام فوري
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                كفاءة الموارد
              </Typography>
              <Typography variant="h4">
                {resourceMetrics.efficiency}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={resourceMetrics.efficiency}
                color="success"
                sx={{ mt: 2 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                التنبؤات
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingUp color="primary" />
                <Typography variant="body2" sx={{ ml: 1 }}>
                  تحليل الاتجاهات نشط
                </Typography>
              </Box>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<Timeline />}
                sx={{ mt: 2 }}
              >
                عرض التفاصيل
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Resource Table */}
        <Grid item xs={12}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>المورد</TableCell>
                  <TableCell>الكمية</TableCell>
                  <TableCell>الحالة</TableCell>
                  <TableCell>التنبؤ</TableCell>
                  <TableCell>آخر تحديث</TableCell>
                  <TableCell>الإجراءات</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {resources.map((resource) => (
                  <TableRow key={resource.id}>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Inventory sx={{ mr: 1 }} />
                        <Box>
                          <Typography variant="body1">
                            {resource.name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {resource.category}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box>
                        <Typography variant="body2">
                          {resource.quantity} {resource.unit}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={(resource.quantity / resource.maxThreshold) * 100}
                          color={getStatusColor(resource.status)}
                          sx={{ mt: 1, height: 4, borderRadius: 2 }}
                        />
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={resource.status}
                        color={getStatusColor(resource.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {predictions.find(p => p.resourceId === resource.id)?.predictedDemand || '-'}
                    </TableCell>
                    <TableCell>
                      {new Date(resource.lastUpdated).toLocaleDateString('ar-SA')}
                    </TableCell>
                    <TableCell>
                      <IconButton size="small" onClick={() => setSelectedResource(resource)}>
                        <Edit />
                      </IconButton>
                      <IconButton size="small" color="error">
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>
      </Grid>

      {/* Add/Edit Resource Dialog */}
      <Dialog
        open={addResourceDialog}
        onClose={() => setAddResourceDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedResource ? 'تعديل مورد' : 'إضافة مورد جديد'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="اسم المورد"
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                select
                label="الفئة"
                margin="normal"
              >
                <MenuItem value="medical">مستلزمات طبية</MenuItem>
                <MenuItem value="equipment">معدات</MenuItem>
                <MenuItem value="medicine">أدوية</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="الكمية"
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="الوحدة"
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="الحد الأدنى"
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="الحد الأقصى"
                margin="normal"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddResourceDialog(false)}>إلغاء</Button>
          <Button variant="contained" color="primary">
            {selectedResource ? 'تحديث' : 'إضافة'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AdvancedResourceManagement;

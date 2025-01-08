import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Favorite as HeartIcon,
  ShowChart as ChartIcon,
} from '@mui/icons-material';
import { Line } from 'react-chartjs-2';
import { useTranslation } from 'react-i18next';
import { format } from 'date-fns';
import { ar } from 'date-fns/locale';

interface VitalSign {
  id: string;
  type: string;
  value: number;
  unit: string;
  timestamp: Date;
  notes: string;
}

interface VitalSignType {
  id: string;
  name: string;
  unit: string;
  normalRange: {
    min: number;
    max: number;
  };
}

const vitalSignTypes: VitalSignType[] = [
  {
    id: 'bloodPressure',
    name: 'ضغط الدم',
    unit: 'mmHg',
    normalRange: { min: 90, max: 120 },
  },
  {
    id: 'heartRate',
    name: 'معدل ضربات القلب',
    unit: 'bpm',
    normalRange: { min: 60, max: 100 },
  },
  {
    id: 'temperature',
    name: 'درجة الحرارة',
    unit: '°C',
    normalRange: { min: 36.1, max: 37.2 },
  },
  {
    id: 'oxygenSaturation',
    name: 'تشبع الأكسجين',
    unit: '%',
    normalRange: { min: 95, max: 100 },
  },
];

const VitalSignsTracker: React.FC = () => {
  const { t } = useTranslation();
  const [vitalSigns, setVitalSigns] = useState<VitalSign[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedType, setSelectedType] = useState<string>('');
  const [currentValue, setCurrentValue] = useState<string>('');
  const [notes, setNotes] = useState<string>('');
  const [showChart, setShowChart] = useState(false);
  const [selectedVitalSign, setSelectedVitalSign] = useState<VitalSignType | null>(null);

  useEffect(() => {
    // Load vital signs from local storage
    const savedVitalSigns = localStorage.getItem('vitalSigns');
    if (savedVitalSigns) {
      setVitalSigns(JSON.parse(savedVitalSigns));
    }
  }, []);

  useEffect(() => {
    // Save vital signs to local storage
    localStorage.setItem('vitalSigns', JSON.stringify(vitalSigns));
  }, [vitalSigns]);

  const handleAddVitalSign = () => {
    if (!selectedType || !currentValue) return;

    const newVitalSign: VitalSign = {
      id: Date.now().toString(),
      type: selectedType,
      value: parseFloat(currentValue),
      unit: vitalSignTypes.find(t => t.id === selectedType)?.unit || '',
      timestamp: new Date(),
      notes,
    };

    setVitalSigns(prev => [...prev, newVitalSign]);
    handleCloseDialog();
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedType('');
    setCurrentValue('');
    setNotes('');
  };

  const handleDeleteVitalSign = (id: string) => {
    setVitalSigns(prev => prev.filter(vs => vs.id !== id));
  };

  const getVitalSignStatus = (type: string, value: number): 'normal' | 'warning' | 'danger' => {
    const vitalSignType = vitalSignTypes.find(t => t.id === type);
    if (!vitalSignType) return 'normal';

    const { min, max } = vitalSignType.normalRange;
    if (value < min * 0.9 || value > max * 1.1) return 'danger';
    if (value < min || value > max) return 'warning';
    return 'normal';
  };

  const renderChart = () => {
    if (!selectedVitalSign) return null;

    const relevantSigns = vitalSigns
      .filter(vs => vs.type === selectedVitalSign.id)
      .sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());

    const data = {
      labels: relevantSigns.map(vs =>
        format(new Date(vs.timestamp), 'MM/dd HH:mm', { locale: ar })
      ),
      datasets: [
        {
          label: selectedVitalSign.name,
          data: relevantSigns.map(vs => vs.value),
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        },
      ],
    };

    return (
      <Dialog open={showChart} onClose={() => setShowChart(false)} maxWidth="md" fullWidth>
        <DialogTitle>{t('vitalSigns.chart.title', { type: selectedVitalSign.name })}</DialogTitle>
        <DialogContent>
          <Line
            data={data}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
              },
              scales: {
                y: {
                  beginAtZero: false,
                },
              },
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowChart(false)}>{t('common.close')}</Button>
        </DialogActions>
      </Dialog>
    );
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h5">{t('vitalSigns.title')}</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          {t('vitalSigns.addNew')}
        </Button>
      </Box>

      <Grid container spacing={3}>
        {vitalSignTypes.map(type => {
          const latestSign = vitalSigns
            .filter(vs => vs.type === type.id)
            .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())[0];

          return (
            <Grid item xs={12} sm={6} md={3} key={type.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6">{type.name}</Typography>
                    <IconButton
                      onClick={() => {
                        setSelectedVitalSign(type);
                        setShowChart(true);
                      }}
                    >
                      <ChartIcon />
                    </IconButton>
                  </Box>
                  {latestSign ? (
                    <>
                      <Typography variant="h4" component="div" gutterBottom>
                        {latestSign.value} {type.unit}
                      </Typography>
                      <Typography color="textSecondary" variant="body2">
                        {format(new Date(latestSign.timestamp), 'PPpp', { locale: ar })}
                      </Typography>
                    </>
                  ) : (
                    <Typography color="textSecondary">
                      {t('vitalSigns.noData')}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <Paper sx={{ mt: 3, p: 2 }}>
        <Typography variant="h6" gutterBottom>
          {t('vitalSigns.history')}
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>{t('vitalSigns.type')}</TableCell>
                <TableCell align="right">{t('vitalSigns.value')}</TableCell>
                <TableCell>{t('vitalSigns.timestamp')}</TableCell>
                <TableCell>{t('vitalSigns.notes')}</TableCell>
                <TableCell align="right">{t('common.actions')}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {vitalSigns
                .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
                .map(sign => (
                  <TableRow key={sign.id}>
                    <TableCell>
                      {vitalSignTypes.find(t => t.id === sign.type)?.name}
                    </TableCell>
                    <TableCell align="right">
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
                        <HeartIcon
                          sx={{
                            mr: 1,
                            color: {
                              normal: 'success.main',
                              warning: 'warning.main',
                              danger: 'error.main',
                            }[getVitalSignStatus(sign.type, sign.value)],
                          }}
                        />
                        {sign.value} {sign.unit}
                      </Box>
                    </TableCell>
                    <TableCell>
                      {format(new Date(sign.timestamp), 'PPpp', { locale: ar })}
                    </TableCell>
                    <TableCell>{sign.notes}</TableCell>
                    <TableCell align="right">
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteVitalSign(sign.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{t('vitalSigns.addNew')}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label={t('vitalSigns.type')}
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                SelectProps={{
                  native: true,
                }}
              >
                <option value="">{t('common.select')}</option>
                {vitalSignTypes.map(type => (
                  <option key={type.id} value={type.id}>
                    {type.name} ({type.unit})
                  </option>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                type="number"
                label={t('vitalSigns.value')}
                value={currentValue}
                onChange={(e) => setCurrentValue(e.target.value)}
                InputProps={{
                  endAdornment: selectedType
                    ? vitalSignTypes.find(t => t.id === selectedType)?.unit
                    : '',
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label={t('vitalSigns.notes')}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>{t('common.cancel')}</Button>
          <Button
            onClick={handleAddVitalSign}
            variant="contained"
            disabled={!selectedType || !currentValue}
          >
            {t('common.save')}
          </Button>
        </DialogActions>
      </Dialog>

      {renderChart()}
    </Container>
  );
};

export default VitalSignsTracker;

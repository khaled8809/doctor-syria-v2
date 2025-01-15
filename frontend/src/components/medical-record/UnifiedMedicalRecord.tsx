import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Tabs,
  Tab,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from '@mui/material';
import {
  Person,
  LocalHospital,
  Science,
  Medication,
  Event,
  Share,
  Download,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  FileUpload,
  History,
  Assessment,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { format } from 'date-fns';
import { ar } from 'date-fns/locale';

interface MedicalRecord {
  personalInfo: {
    name: string;
    dateOfBirth: string;
    gender: string;
    bloodType: string;
    weight: number;
    height: number;
  };
  allergies: string[];
  chronicConditions: string[];
  medications: {
    name: string;
    dosage: string;
    frequency: string;
    startDate: string;
    endDate?: string;
  }[];
  visits: {
    date: string;
    doctor: string;
    diagnosis: string;
    prescription: string[];
    notes: string;
  }[];
  labResults: {
    date: string;
    type: string;
    result: string;
    normalRange: string;
    status: 'normal' | 'abnormal';
    file?: string;
  }[];
  vaccinations: {
    name: string;
    date: string;
    nextDue?: string;
  }[];
}

const UnifiedMedicalRecord: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState(0);
  const [record, setRecord] = useState<MedicalRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [showShareDialog, setShowShareDialog] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState('');

  useEffect(() => {
    fetchMedicalRecord();
  }, []);

  const fetchMedicalRecord = async () => {
    try {
      // This would be replaced with actual API call
      const mockRecord: MedicalRecord = {
        personalInfo: {
          name: 'أحمد محمد',
          dateOfBirth: '1990-05-15',
          gender: 'ذكر',
          bloodType: 'A+',
          weight: 75,
          height: 175,
        },
        allergies: ['البنسلين', 'حبوب اللقاح'],
        chronicConditions: ['ضغط الدم المرتفع'],
        medications: [
          {
            name: 'أملوديبين',
            dosage: '5mg',
            frequency: 'مرة واحدة يومياً',
            startDate: '2024-12-01',
          },
        ],
        visits: [
          {
            date: '2024-12-15',
            doctor: 'د. سمير حسن',
            diagnosis: 'التهاب الجيوب الأنفية',
            prescription: ['أموكسيسيلين 500mg', 'بخاخ أنف'],
            notes: 'تحسن ملحوظ في الأعراض',
          },
        ],
        labResults: [
          {
            date: '2024-12-10',
            type: 'تحليل الدم الكامل',
            result: '14.5',
            normalRange: '13.5-17.5',
            status: 'normal',
          },
        ],
        vaccinations: [
          {
            name: 'لقاح الإنفلونزا',
            date: '2024-11-01',
            nextDue: '2025-11-01',
          },
        ],
      };
      setRecord(mockRecord);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching medical record:', error);
      setLoading(false);
    }
  };

  const handleShareRecord = () => {
    // Implement sharing functionality
    setShowShareDialog(false);
  };

  const handleDownloadRecord = () => {
    // Implement download functionality
  };

  const renderPersonalInfo = () => {
    if (!record) return null;

    return (
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h6">{t('medicalRecord.personalInfo')}</Typography>
          <IconButton>
            <EditIcon />
          </IconButton>
        </Box>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="textSecondary">
              {t('medicalRecord.name')}
            </Typography>
            <Typography variant="body1">{record.personalInfo.name}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="textSecondary">
              {t('medicalRecord.dateOfBirth')}
            </Typography>
            <Typography variant="body1">
              {format(new Date(record.personalInfo.dateOfBirth), 'PP', { locale: ar })}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="textSecondary">
              {t('medicalRecord.gender')}
            </Typography>
            <Typography variant="body1">{record.personalInfo.gender}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="textSecondary">
              {t('medicalRecord.bloodType')}
            </Typography>
            <Typography variant="body1">{record.personalInfo.bloodType}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="textSecondary">
              {t('medicalRecord.weight')}
            </Typography>
            <Typography variant="body1">{record.personalInfo.weight} kg</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="textSecondary">
              {t('medicalRecord.height')}
            </Typography>
            <Typography variant="body1">{record.personalInfo.height} cm</Typography>
          </Grid>
        </Grid>

        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            {t('medicalRecord.allergies')}
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {record.allergies.map((allergy, index) => (
              <Chip
                key={index}
                label={allergy}
                color="error"
                variant="outlined"
                onDelete={() => {}}
              />
            ))}
            <Chip
              icon={<AddIcon />}
              label={t('medicalRecord.addAllergy')}
              onClick={() => {}}
              variant="outlined"
            />
          </Box>
        </Box>

        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            {t('medicalRecord.chronicConditions')}
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {record.chronicConditions.map((condition, index) => (
              <Chip
                key={index}
                label={condition}
                color="primary"
                variant="outlined"
                onDelete={() => {}}
              />
            ))}
            <Chip
              icon={<AddIcon />}
              label={t('medicalRecord.addCondition')}
              onClick={() => {}}
              variant="outlined"
            />
          </Box>
        </Box>
      </Paper>
    );
  };

  const renderMedications = () => {
    if (!record) return null;

    return (
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h6">{t('medicalRecord.medications')}</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {}}
          >
            {t('medicalRecord.addMedication')}
          </Button>
        </Box>
        <List>
          {record.medications.map((medication, index) => (
            <React.Fragment key={index}>
              <ListItem>
                <ListItemIcon>
                  <Medication />
                </ListItemIcon>
                <ListItemText
                  primary={medication.name}
                  secondary={
                    <React.Fragment>
                      <Typography variant="body2">
                        {medication.dosage} - {medication.frequency}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {t('medicalRecord.startDate')}: {format(new Date(medication.startDate), 'PP', { locale: ar })}
                      </Typography>
                    </React.Fragment>
                  }
                />
                <IconButton>
                  <EditIcon />
                </IconButton>
                <IconButton>
                  <DeleteIcon />
                </IconButton>
              </ListItem>
              {index < record.medications.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </Paper>
    );
  };

  const renderVisits = () => {
    if (!record) return null;

    return (
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h6">{t('medicalRecord.visits')}</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {}}
          >
            {t('medicalRecord.addVisit')}
          </Button>
        </Box>
        <List>
          {record.visits.map((visit, index) => (
            <React.Fragment key={index}>
              <ListItem>
                <ListItemIcon>
                  <Event />
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Typography variant="subtitle1">
                        {format(new Date(visit.date), 'PP', { locale: ar })}
                      </Typography>
                      <Chip
                        label={visit.doctor}
                        size="small"
                        sx={{ ml: 1 }}
                      />
                    </Box>
                  }
                  secondary={
                    <React.Fragment>
                      <Typography variant="body2" color="primary">
                        {visit.diagnosis}
                      </Typography>
                      <Box sx={{ mt: 1 }}>
                        {visit.prescription.map((med, idx) => (
                          <Chip
                            key={idx}
                            label={med}
                            size="small"
                            variant="outlined"
                            sx={{ mr: 1, mb: 1 }}
                          />
                        ))}
                      </Box>
                      <Typography variant="body2" color="textSecondary">
                        {visit.notes}
                      </Typography>
                    </React.Fragment>
                  }
                />
                <IconButton>
                  <EditIcon />
                </IconButton>
              </ListItem>
              {index < record.visits.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </Paper>
    );
  };

  const renderLabResults = () => {
    if (!record) return null;

    return (
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h6">{t('medicalRecord.labResults')}</Typography>
          <Button
            variant="contained"
            startIcon={<FileUpload />}
            onClick={() => {}}
          >
            {t('medicalRecord.uploadResults')}
          </Button>
        </Box>
        <List>
          {record.labResults.map((result, index) => (
            <React.Fragment key={index}>
              <ListItem>
                <ListItemIcon>
                  <Science />
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Typography variant="subtitle1">
                        {result.type}
                      </Typography>
                      <Chip
                        label={result.status === 'normal' ? t('medicalRecord.normal') : t('medicalRecord.abnormal')}
                        color={result.status === 'normal' ? 'success' : 'error'}
                        size="small"
                        sx={{ ml: 1 }}
                      />
                    </Box>
                  }
                  secondary={
                    <React.Fragment>
                      <Typography variant="body2">
                        {t('medicalRecord.result')}: {result.result} ({result.normalRange})
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {format(new Date(result.date), 'PP', { locale: ar })}
                      </Typography>
                    </React.Fragment>
                  }
                />
                {result.file && (
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<Download />}
                    onClick={() => {}}
                  >
                    {t('medicalRecord.download')}
                  </Button>
                )}
              </ListItem>
              {index < record.labResults.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </Paper>
    );
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4">
            {t('medicalRecord.title')}
          </Typography>
          <Box>
            <Button
              variant="outlined"
              startIcon={<Share />}
              onClick={() => setShowShareDialog(true)}
              sx={{ mr: 1 }}
            >
              {t('medicalRecord.share')}
            </Button>
            <Button
              variant="outlined"
              startIcon={<Download />}
              onClick={handleDownloadRecord}
            >
              {t('medicalRecord.download')}
            </Button>
          </Box>
        </Box>

        <Paper sx={{ mb: 3 }}>
          <Tabs
            value={activeTab}
            onChange={(_, newValue) => setActiveTab(newValue)}
            variant="scrollable"
            scrollButtons="auto"
          >
            <Tab icon={<Person />} label={t('medicalRecord.tabs.personal')} />
            <Tab icon={<Medication />} label={t('medicalRecord.tabs.medications')} />
            <Tab icon={<History />} label={t('medicalRecord.tabs.visits')} />
            <Tab icon={<Assessment />} label={t('medicalRecord.tabs.labResults')} />
          </Tabs>
        </Paper>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Box>
            {activeTab === 0 && renderPersonalInfo()}
            {activeTab === 1 && renderMedications()}
            {activeTab === 2 && renderVisits()}
            {activeTab === 3 && renderLabResults()}
          </Box>
        )}
      </Box>

      {/* Share Dialog */}
      <Dialog open={showShareDialog} onClose={() => setShowShareDialog(false)}>
        <DialogTitle>{t('medicalRecord.shareRecord')}</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>{t('medicalRecord.selectDoctor')}</InputLabel>
            <Select
              value={selectedDoctor}
              onChange={(e) => setSelectedDoctor(e.target.value)}
            >
              <MenuItem value="doctor1">د. سمير حسن</MenuItem>
              <MenuItem value="doctor2">د. ليلى أحمد</MenuItem>
              <MenuItem value="doctor3">د. محمد علي</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowShareDialog(false)}>
            {t('common.cancel')}
          </Button>
          <Button
            variant="contained"
            onClick={handleShareRecord}
            disabled={!selectedDoctor}
          >
            {t('medicalRecord.share')}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default UnifiedMedicalRecord;

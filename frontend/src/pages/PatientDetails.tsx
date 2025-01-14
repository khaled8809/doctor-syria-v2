import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Tabs,
  Tab,
  Button,
  Chip,
  IconButton,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  Edit,
  LocalHospital,
  Assignment,
  Timeline,
  Description,
  Add,
  Download,
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { usePatient } from '../hooks/usePatient';
import PDFDownloadButton from '../components/common/PDFDownloadButton';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`patient-tabpanel-${index}`}
      aria-labelledby={`patient-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const PatientDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { patient, loading, error } = usePatient(id!);
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (loading) {
    return <Typography>جاري التحميل...</Typography>;
  }

  if (error || !patient) {
    return <Typography color="error">حدث خطأ في تحميل بيانات المريض</Typography>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">تفاصيل المريض</Typography>
        <Box>
          <PDFDownloadButton contentId="patient-details" />
          <Button
            variant="contained"
            startIcon={<Edit />}
            sx={{ mr: 1 }}
            onClick={() => navigate(`/patients/${id}/edit`)}
          >
            تعديل
          </Button>
        </Box>
      </Box>

      <div id="patient-details">
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Box>
                  <Typography variant="h5">{patient.name}</Typography>
                  <Chip
                    label={patient.status}
                    color={
                      patient.status === 'active'
                        ? 'success'
                        : patient.status === 'inactive'
                        ? 'error'
                        : 'warning'
                    }
                    sx={{ mt: 1 }}
                  />
                </Box>
                <Box sx={{ mt: 2 }}>
                  <Typography color="textSecondary">رقم الملف: {patient.id}</Typography>
                  <Typography color="textSecondary">العمر: {patient.age} سنة</Typography>
                  <Typography color="textSecondary">الجنس: {patient.gender}</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Box sx={{ textAlign: 'right' }}>
                  <Typography color="textSecondary">
                    آخر زيارة: {new Date(patient.lastVisit).toLocaleDateString('ar-SA')}
                  </Typography>
                  <Typography color="textSecondary">الهاتف: {patient.phone}</Typography>
                  <Typography color="textSecondary">البريد: {patient.email}</Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="patient tabs">
            <Tab icon={<LocalHospital />} label="السجل الطبي" />
            <Tab icon={<Assignment />} label="الوصفات الطبية" />
            <Tab icon={<Timeline />} label="المؤشرات الحيوية" />
            <Tab icon={<Description />} label="التقارير" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">السجل الطبي</Typography>
            <Button startIcon={<Add />} variant="contained">
              إضافة سجل
            </Button>
          </Box>
          <List>
            {patient.medicalRecords?.map((record: any) => (
              <React.Fragment key={record.id}>
                <ListItem>
                  <ListItemText
                    primary={record.diagnosis}
                    secondary={new Date(record.date).toLocaleDateString('ar-SA')}
                  />
                  <ListItemSecondaryAction>
                    <IconButton edge="end" aria-label="download">
                      <Download />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">الوصفات الطبية</Typography>
            <Button startIcon={<Add />} variant="contained">
              إضافة وصفة
            </Button>
          </Box>
          <List>
            {patient.prescriptions?.map((prescription: any) => (
              <React.Fragment key={prescription.id}>
                <ListItem>
                  <ListItemText
                    primary={prescription.medication}
                    secondary={`${prescription.dosage} - ${prescription.frequency}`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton edge="end" aria-label="download">
                      <Download />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">المؤشرات الحيوية</Typography>
            <Button startIcon={<Add />} variant="contained">
              إضافة قياس
            </Button>
          </Box>
          <Grid container spacing={3}>
            {patient.vitals?.map((vital: any) => (
              <Grid item xs={12} sm={6} md={3} key={vital.id}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      {vital.name}
                    </Typography>
                    <Typography variant="h5">{vital.value}</Typography>
                    <Typography variant="caption">
                      {new Date(vital.timestamp).toLocaleString('ar-SA')}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">التقارير</Typography>
            <Button startIcon={<Add />} variant="contained">
              إضافة تقرير
            </Button>
          </Box>
          <List>
            {patient.reports?.map((report: any) => (
              <React.Fragment key={report.id}>
                <ListItem>
                  <ListItemText
                    primary={report.title}
                    secondary={new Date(report.date).toLocaleDateString('ar-SA')}
                  />
                  <ListItemSecondaryAction>
                    <IconButton edge="end" aria-label="download">
                      <Download />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </TabPanel>
      </div>
    </Box>
  );
};

export default PatientDetails;

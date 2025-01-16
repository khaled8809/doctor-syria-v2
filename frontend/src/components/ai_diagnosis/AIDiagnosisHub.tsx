import React, { useState, useEffect } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
  Divider,
  Button,
  Alert,
  Drawer,
  IconButton,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Menu as MenuIcon,
  LocalHospital,
  Timeline,
  Assessment,
  Notifications,
} from '@mui/icons-material';
import DiagnosisSession from './DiagnosisSession';
import DiagnosisResults from './DiagnosisResults';
import DiagnosisChart from './DiagnosisChart';
import MedicalHistory from './MedicalHistory';
import HealthRiskPredictor from './HealthRiskPredictor';
import ResourcePredictor from './ResourcePredictor';
import FollowUpReminder from './FollowUpReminder';
import { usePatientContext } from '../../contexts/PatientContext';
import { useAIService } from '../../services/ai-service';
import { useMedicalRecordService } from '../../services/medical-record-service';
import { useNotificationService } from '../../services/notification-service';
import { DiagnosisResult, SymptomInput } from '../../types/diagnosis';
import { Patient } from '../../types/patient';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

interface DiagnosisStartParams {
  patientId: string;
  symptoms: SymptomInput[];
}

interface MedicalRecordSaveParams {
  patientId: string;
  diagnosisResults: DiagnosisResult[];
  symptoms?: SymptomInput[];
}

interface NotificationParams {
  type: 'high_risk_diagnosis';
  recipientId: string;
  data: {
    patientName: string;
    diagnosisId: string;
  };
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`ai-diagnosis-tabpanel-${index}`}
      aria-labelledby={`ai-diagnosis-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function AIDiagnosisHub() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [activeTab, setActiveTab] = useState(0);
  const [drawerOpen, setDrawerOpen] = useState(!isMobile);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [diagnosisResults, setDiagnosisResults] = useState<DiagnosisResult[] | null>(null);

  const { currentPatient } = usePatientContext();
  const { startDiagnosis } = useAIService();
  const { saveMedicalRecord } = useMedicalRecordService();
  const { sendNotification } = useNotificationService();

  useEffect(() => {
    if (!currentPatient) {
      setError('Please select a patient first');
    } else {
      setError(null);
    }
  }, [currentPatient]);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleStartDiagnosis = async (symptoms: SymptomInput[]) => {
    if (!currentPatient) return;

    setLoading(true);
    setError(null);

    try {
      const results = await startDiagnosis({
        patientId: currentPatient.id,
        symptoms,
      } as DiagnosisStartParams);

      setDiagnosisResults(results);

      // Save to medical record
      await saveMedicalRecord({
        patientId: currentPatient.id,
        diagnosisResults: results,
        symptoms,
      } as MedicalRecordSaveParams);

      // Send notification to attending physician
      if (results.some((r) => r.riskLevel === 'high')) {
        await sendNotification({
          type: 'high_risk_diagnosis',
          recipientId: currentPatient.doctorId,
          data: {
            patientName: `${currentPatient.firstName} ${currentPatient.lastName}`,
            diagnosisId: results[0].id,
          },
        } as NotificationParams);
      }

      setActiveTab(1); // Switch to results tab
    } catch (err) {
      setError('An error occurred during diagnosis');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveToRecord = async () => {
    if (!currentPatient || !diagnosisResults) return;

    try {
      await saveMedicalRecord({
        patientId: currentPatient.id,
        diagnosisResults,
      } as MedicalRecordSaveParams);
    } catch (err) {
      setError('An error occurred while saving results');
    }
  };

  const renderDrawerContent = () => (
    <Box sx={{ width: 250, p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Medical AI Assistant
      </Typography>
      <Divider sx={{ my: 2 }} />
      <Tabs
        orientation="vertical"
        value={activeTab}
        onChange={handleTabChange}
        sx={{ borderRight: 1, borderColor: 'divider' }}
      >
        <Tab
          icon={<LocalHospital />}
          label="Diagnosis Session"
          id="ai-diagnosis-tab-0"
          aria-controls="ai-diagnosis-tabpanel-0"
        />
        <Tab
          icon={<Assessment />}
          label="Diagnosis Results"
          id="ai-diagnosis-tab-1"
          aria-controls="ai-diagnosis-tabpanel-1"
        />
        <Tab
          icon={<Timeline />}
          label="Risk Indicators"
          id="ai-diagnosis-tab-2"
          aria-controls="ai-diagnosis-tabpanel-2"
        />
        <Tab
          icon={<Notifications />}
          label="Follow-up"
          id="ai-diagnosis-tab-3"
          aria-controls="ai-diagnosis-tabpanel-3"
        />
      </Tabs>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {isMobile ? (
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={() => setDrawerOpen(!drawerOpen)}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
      ) : null}

      <Drawer
        variant={isMobile ? 'temporary' : 'permanent'}
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        {renderDrawerContent()}
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Paper sx={{ width: '100%', mb: 2 }}>
          <TabPanel value={activeTab} index={0}>
            <DiagnosisSession
              onDiagnosisStart={handleStartDiagnosis}
              loading={loading}
            />
          </TabPanel>

          <TabPanel value={activeTab} index={1}>
            {diagnosisResults && (
              <>
                <DiagnosisResults results={diagnosisResults} />
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSaveToRecord}
                  sx={{ mt: 2 }}
                >
                  Save to Medical Record
                </Button>
              </>
            )}
          </TabPanel>

          <TabPanel value={activeTab} index={2}>
            <HealthRiskPredictor />
          </TabPanel>

          <TabPanel value={activeTab} index={3}>
            <FollowUpReminder />
          </TabPanel>
        </Paper>
      </Box>
    </Box>
  );
}

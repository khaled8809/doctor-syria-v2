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
  Settings,
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

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
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
  const [diagnosisResults, setDiagnosisResults] = useState<any>(null);

  const { currentPatient } = usePatientContext();
  const { startDiagnosis } = useAIService();
  const { saveMedicalRecord } = useMedicalRecordService();
  const { sendNotification } = useNotificationService();

  useEffect(() => {
    if (!currentPatient) {
      setError('الرجاء اختيار مريض أولاً');
    } else {
      setError(null);
    }
  }, [currentPatient]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleStartDiagnosis = async (symptoms: any[]) => {
    if (!currentPatient) return;

    setLoading(true);
    setError(null);

    try {
      const results = await startDiagnosis({
        patientId: currentPatient.id,
        symptoms,
      });

      setDiagnosisResults(results);

      // حفظ في السجل الطبي
      await saveMedicalRecord({
        patientId: currentPatient.id,
        diagnosisResults: results,
        symptoms,
      });

      // إرسال إشعار للطبيب المعالج
      if (results.some((r: any) => r.disease.risk_level >= 2)) {
        await sendNotification({
          type: 'high_risk_diagnosis',
          recipientId: currentPatient.doctorId,
          data: {
            patientName: currentPatient.name,
            diagnosisId: results[0].id,
          },
        });
      }

      setActiveTab(1); // الانتقال إلى تب النتائج
    } catch (err) {
      setError('حدث خطأ أثناء التشخيص');
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
      });
    } catch (err) {
      setError('حدث خطأ أثناء حفظ النتائج');
    }
  };

  const renderDrawerContent = () => (
    <Box sx={{ width: 250, p: 2 }}>
      <Typography variant="h6" gutterBottom>
        الذكاء الاصطناعي الطبي
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
          label="التشخيص"
          id="ai-diagnosis-tab-0"
        />
        <Tab
          icon={<Assessment />}
          label="النتائج"
          id="ai-diagnosis-tab-1"
          disabled={!diagnosisResults}
        />
        <Tab
          icon={<Timeline />}
          label="التحليلات"
          id="ai-diagnosis-tab-2"
        />
        <Tab
          icon={<Notifications />}
          label="المتابعة"
          id="ai-diagnosis-tab-3"
        />
      </Tabs>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {isMobile ? (
        <Drawer
          variant="temporary"
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
        >
          {renderDrawerContent()}
        </Drawer>
      ) : (
        <Drawer
          variant="permanent"
          sx={{
            width: 250,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: 250,
              boxSizing: 'border-box',
            },
          }}
        >
          {renderDrawerContent()}
        </Drawer>
      )}

      <Box sx={{ flexGrow: 1, p: 3 }}>
        {isMobile && (
          <IconButton
            edge="start"
            onClick={() => setDrawerOpen(true)}
            sx={{ mb: 2 }}
          >
            <MenuIcon />
          </IconButton>
        )}

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {currentPatient && (
          <Paper sx={{ mb: 3, p: 2 }}>
            <Typography variant="h6">
              المريض: {currentPatient.name}
            </Typography>
            <Typography color="text.secondary">
              رقم الملف: {currentPatient.fileNumber}
            </Typography>
          </Paper>
        )}

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
              <DiagnosisChart data={diagnosisResults} />
              <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  onClick={handleSaveToRecord}
                >
                  حفظ في السجل الطبي
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => setActiveTab(3)}
                >
                  إضافة متابعة
                </Button>
              </Box>
            </>
          )}
        </TabPanel>

        <TabPanel value={activeTab} index={2}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            {currentPatient && (
              <HealthRiskPredictor patientId={currentPatient.id} />
            )}
            <ResourcePredictor />
          </Box>
        </TabPanel>

        <TabPanel value={activeTab} index={3}>
          {currentPatient && diagnosisResults && (
            <FollowUpReminder
              patientId={currentPatient.id}
              diagnosis={diagnosisResults[0].disease}
              onReminderCreate={async (reminder) => {
                try {
                  await sendNotification({
                    type: 'follow_up_reminder',
                    recipientId: currentPatient.id,
                    data: reminder,
                  });
                } catch (err) {
                  setError('حدث خطأ أثناء إنشاء التذكير');
                }
              }}
              onReminderUpdate={async (reminder) => {
                try {
                  await sendNotification({
                    type: 'reminder_update',
                    recipientId: currentPatient.id,
                    data: reminder,
                  });
                } catch (err) {
                  setError('حدث خطأ أثناء تحديث التذكير');
                }
              }}
            />
          )}
        </TabPanel>
      </Box>
    </Box>
  );
}

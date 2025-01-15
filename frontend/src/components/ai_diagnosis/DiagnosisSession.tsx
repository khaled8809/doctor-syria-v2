import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import SymptomSelector from './SymptomSelector';
import DiagnosisResults from './DiagnosisResults';
import { useAIService } from '../../services/ai-service';
import { usePatientContext } from '../../contexts/PatientContext';

const steps = ['اختيار الأعراض', 'التشخيص الأولي', 'النتائج والتوصيات'];

interface DiagnosisResult {
  id: string;
  diagnosis: string;
  confidence: number;
  recommendations: string[];
  riskLevel: 'low' | 'medium' | 'high';
}

export default function DiagnosisSession() {
  const [activeStep, setActiveStep] = useState(0);
  const [diagnosisResults, setDiagnosisResults] = useState<DiagnosisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { startDiagnosis } = useAIService();
  const { currentPatient } = usePatientContext();

  const handleDiagnosisStart = async (symptoms: string[]) => {
    setError(null);
    setLoading(true);

    try {
      const results = await startDiagnosis({
        patientId: currentPatient?.id || '',
        symptoms,
      });
      setDiagnosisResults(results);
      setActiveStep((prevStep) => prevStep + 1);
    } catch (err) {
      setError('حدث خطأ أثناء التشخيص. الرجاء المحاولة مرة أخرى.');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
    setError(null);
  };

  return (
    <Box sx={{ width: '100%', p: 3 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          التشخيص الذكي
        </Typography>

        {currentPatient && (
          <Typography variant="h6" gutterBottom>
            المريض: {currentPatient.name}
          </Typography>
        )}

        <Stepper activeStep={activeStep} sx={{ my: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ mt: 2, minHeight: '400px' }}>
          {activeStep === 0 && (
            <SymptomSelector
              onDiagnosisStart={handleDiagnosisStart}
              loading={loading}
            />
          )}

          {activeStep === 1 && (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="h6" gutterBottom>
                جاري تحليل الأعراض...
              </Typography>
              <CircularProgress />
            </Box>
          )}

          {activeStep === 2 && diagnosisResults && (
            <DiagnosisResults results={diagnosisResults} />
          )}
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 4 }}>
          <Button
            disabled={activeStep === 0}
            onClick={handleBack}
            sx={{ mr: 1 }}
          >
            رجوع
          </Button>
          <Button
            variant="contained"
            onClick={() => setActiveStep((prev) => prev + 1)}
            disabled={loading || activeStep === steps.length - 1}
          >
            {activeStep === steps.length - 1 ? 'إنهاء' : 'التالي'}
            {loading && <CircularProgress size={24} sx={{ ml: 1 }} />}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}

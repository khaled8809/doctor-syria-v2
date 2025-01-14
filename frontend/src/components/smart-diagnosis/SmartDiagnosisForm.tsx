import React, { useState } from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  Typography,
  Paper,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Chip,
  Autocomplete,
  CircularProgress,
  Alert,
} from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';

interface Symptom {
  id: string;
  name: string;
  severity: number;
  duration: string;
}

const SmartDiagnosisForm: React.FC = () => {
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);
  const [symptoms, setSymptoms] = useState<Symptom[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const steps = [
    {
      label: t('diagnosis.steps.basic'),
      description: t('diagnosis.steps.basicDesc'),
    },
    {
      label: t('diagnosis.steps.symptoms'),
      description: t('diagnosis.steps.symptomsDesc'),
    },
    {
      label: t('diagnosis.steps.history'),
      description: t('diagnosis.steps.historyDesc'),
    },
    {
      label: t('diagnosis.steps.analysis'),
      description: t('diagnosis.steps.analysisDesc'),
    },
  ];

  const commonSymptoms = [
    { id: '1', name: 'حمى', category: 'عام' },
    { id: '2', name: 'صداع', category: 'عام' },
    { id: '3', name: 'سعال', category: 'تنفسي' },
    { id: '4', name: 'تعب', category: 'عام' },
    // يمكن إضافة المزيد من الأعراض
  ];

  const handleNext = async () => {
    if (activeStep === steps.length - 1) {
      setLoading(true);
      try {
        // هنا يتم إرسال البيانات للتحليل
        const response = await analyzeSymptomsWithAI(symptoms);
        setResult(response);
      } catch (error) {
        console.error('Error analyzing symptoms:', error);
      } finally {
        setLoading(false);
      }
    } else {
      setActiveStep((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const analyzeSymptomsWithAI = async (symptoms: Symptom[]) => {
    // محاكاة تحليل الأعراض باستخدام الذكاء الاصطناعي
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          possibleConditions: [
            {
              name: 'نزلة برد',
              probability: 0.75,
              urgency: 'متوسطة',
              recommendedAction: 'استشارة طبيب عام',
            },
          ],
          recommendedSpecialties: ['طب عام', 'أنف وأذن وحنجرة'],
          estimatedConsultationTime: 20,
        });
      }, 2000);
    });
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box sx={{ p: 3 }}>
            <TextField
              fullWidth
              label={t('diagnosis.form.age')}
              type="number"
              margin="normal"
            />
            <FormControl component="fieldset" sx={{ mt: 2 }}>
              <FormLabel component="legend">{t('diagnosis.form.gender')}</FormLabel>
              <RadioGroup row>
                <FormControlLabel
                  value="male"
                  control={<Radio />}
                  label={t('diagnosis.form.male')}
                />
                <FormControlLabel
                  value="female"
                  control={<Radio />}
                  label={t('diagnosis.form.female')}
                />
              </RadioGroup>
            </FormControl>
          </Box>
        );

      case 1:
        return (
          <Box sx={{ p: 3 }}>
            <Autocomplete
              multiple
              options={commonSymptoms}
              getOptionLabel={(option) => option.name}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label={t('diagnosis.form.symptoms')}
                  placeholder={t('diagnosis.form.selectSymptoms')}
                />
              )}
              renderTags={(value, getTagProps) =>
                value.map((option, index) => (
                  <Chip
                    label={option.name}
                    {...getTagProps({ index })}
                    color="primary"
                  />
                ))
              }
              onChange={(_, newValue) => {
                setSymptoms(
                  newValue.map((symptom) => ({
                    id: symptom.id,
                    name: symptom.name,
                    severity: 0,
                    duration: '',
                  }))
                );
              }}
            />
            {symptoms.map((symptom) => (
              <Box key={symptom.id} sx={{ mt: 2 }}>
                <Typography variant="subtitle1">{symptom.name}</Typography>
                <FormControl fullWidth sx={{ mt: 1 }}>
                  <FormLabel>{t('diagnosis.form.severity')}</FormLabel>
                  <RadioGroup
                    row
                    value={symptom.severity}
                    onChange={(e) => {
                      const newSymptoms = symptoms.map((s) =>
                        s.id === symptom.id
                          ? { ...s, severity: Number(e.target.value) }
                          : s
                      );
                      setSymptoms(newSymptoms);
                    }}
                  >
                    <FormControlLabel
                      value={1}
                      control={<Radio />}
                      label={t('diagnosis.form.mild')}
                    />
                    <FormControlLabel
                      value={2}
                      control={<Radio />}
                      label={t('diagnosis.form.moderate')}
                    />
                    <FormControlLabel
                      value={3}
                      control={<Radio />}
                      label={t('diagnosis.form.severe')}
                    />
                  </RadioGroup>
                </FormControl>
                <TextField
                  fullWidth
                  label={t('diagnosis.form.duration')}
                  value={symptom.duration}
                  onChange={(e) => {
                    const newSymptoms = symptoms.map((s) =>
                      s.id === symptom.id
                        ? { ...s, duration: e.target.value }
                        : s
                    );
                    setSymptoms(newSymptoms);
                  }}
                  sx={{ mt: 1 }}
                />
              </Box>
            ))}
          </Box>
        );

      case 2:
        return (
          <Box sx={{ p: 3 }}>
            <TextField
              fullWidth
              multiline
              rows={4}
              label={t('diagnosis.form.medicalHistory')}
              margin="normal"
            />
            <TextField
              fullWidth
              multiline
              rows={4}
              label={t('diagnosis.form.medications')}
              margin="normal"
            />
            <TextField
              fullWidth
              multiline
              rows={4}
              label={t('diagnosis.form.allergies')}
              margin="normal"
            />
          </Box>
        );

      case 3:
        return (
          <Box sx={{ p: 3 }}>
            {loading ? (
              <Box sx={{ textAlign: 'center', py: 3 }}>
                <CircularProgress />
                <Typography sx={{ mt: 2 }}>
                  {t('diagnosis.analysis.processing')}
                </Typography>
              </Box>
            ) : result ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
              >
                <Alert severity="info" sx={{ mb: 2 }}>
                  {t('diagnosis.analysis.disclaimer')}
                </Alert>
                <Typography variant="h6" gutterBottom>
                  {t('diagnosis.analysis.possibleConditions')}:
                </Typography>
                {result.possibleConditions.map((condition: any, index: number) => (
                  <Paper key={index} sx={{ p: 2, my: 1 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      {condition.name}
                    </Typography>
                    <Typography color="textSecondary">
                      {t('diagnosis.analysis.probability')}: {condition.probability * 100}%
                    </Typography>
                    <Typography color="textSecondary">
                      {t('diagnosis.analysis.urgency')}: {condition.urgency}
                    </Typography>
                    <Typography color="textSecondary">
                      {t('diagnosis.analysis.recommendedAction')}: {condition.recommendedAction}
                    </Typography>
                  </Paper>
                ))}
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    {t('diagnosis.analysis.recommendations')}:
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {result.recommendedSpecialties.map((specialty: string, index: number) => (
                      <Chip key={index} label={specialty} color="primary" />
                    ))}
                  </Box>
                </Box>
              </motion.div>
            ) : null}
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((step, index) => (
            <Step key={index}>
              <StepLabel>{step.label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <AnimatePresence mode="wait">
          <motion.div
            key={activeStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {renderStepContent(activeStep)}
          </motion.div>
        </AnimatePresence>
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3 }}>
          <Button
            disabled={activeStep === 0}
            onClick={handleBack}
            sx={{ mr: 1 }}
          >
            {t('common.back')}
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={loading}
          >
            {activeStep === steps.length - 1
              ? t('common.finish')
              : t('common.next')}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default SmartDiagnosisForm;

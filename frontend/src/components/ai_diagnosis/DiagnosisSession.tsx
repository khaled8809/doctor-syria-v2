import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Paper,
} from '@mui/material';
import { SymptomSelector } from './SymptomSelector';
import { DiagnosisResults } from './DiagnosisResults';
import { useAIService } from '../../services/ai-service';
import { DiagnosisResult, SymptomInput } from '../../types/diagnosis';

export interface DiagnosisSessionProps {
  patientId: string;
  onDiagnosisStart?: (symptoms: SymptomInput[]) => Promise<void>;
  onDiagnosisComplete?: (result: DiagnosisResult) => void;
}

export const DiagnosisSession: React.FC<DiagnosisSessionProps> = ({
  patientId,
  onDiagnosisStart,
  onDiagnosisComplete,
}) => {
  const [selectedSymptoms, setSelectedSymptoms] = useState<SymptomInput[]>([]);
  const [diagnosisResult, setDiagnosisResult] = useState<DiagnosisResult | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { startDiagnosis } = useAIService();

  const handleSubmit = async () => {
    if (selectedSymptoms.length === 0) {
      setError('Please select at least one symptom');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      if (onDiagnosisStart) {
        await onDiagnosisStart(selectedSymptoms);
      }

      const result = await startDiagnosis({
        patientId,
        symptoms: selectedSymptoms,
      });

      setDiagnosisResult(result);

      if (onDiagnosisComplete) {
        onDiagnosisComplete(result);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred during diagnosis');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          New Diagnosis Session
        </Typography>

        <SymptomSelector
          selectedSymptoms={selectedSymptoms}
          onSymptomsChange={setSelectedSymptoms}
          onSubmit={handleSubmit}
          isSubmitting={isSubmitting}
        />

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {isSubmitting && (
          <Box display="flex" justifyContent="center" mt={2}>
            <CircularProgress />
          </Box>
        )}
      </Paper>

      {diagnosisResult && (
        <DiagnosisResults result={diagnosisResult} />
      )}
    </Box>
  );
};

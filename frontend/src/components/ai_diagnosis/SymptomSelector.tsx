import React, { useState } from 'react';
import {
  Box,
  TextField,
  Autocomplete,
  Button,
  Typography,
  Paper,
} from '@mui/material';

interface SymptomSelectorProps {
  onDiagnosisStart: (symptoms: string[]) => Promise<void>;
  loading: boolean;
}

const SymptomSelector: React.FC<SymptomSelectorProps> = ({
  onDiagnosisStart,
  loading,
}) => {
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);

  const commonSymptoms = [
    'Fever',
    'Headache',
    'Cough',
    'Fatigue',
    'Nausea',
    'Dizziness',
    'Chest Pain',
    'Shortness of Breath',
    'Body Aches',
    'Sore Throat',
  ];

  const handleSubmit = async () => {
    if (selectedSymptoms.length > 0) {
      await onDiagnosisStart(selectedSymptoms);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Select Symptoms
      </Typography>
      <Box sx={{ mb: 3 }}>
        <Autocomplete
          multiple
          options={commonSymptoms}
          value={selectedSymptoms}
          onChange={(_, newValue) => setSelectedSymptoms(newValue)}
          renderInput={(params) => (
            <TextField
              {...params}
              variant="outlined"
              label="Search symptoms"
              placeholder="Type to search"
              fullWidth
            />
          )}
          sx={{ mb: 2 }}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={selectedSymptoms.length === 0 || loading}
          fullWidth
        >
          {loading ? 'Analyzing...' : 'Start Diagnosis'}
        </Button>
      </Box>
    </Paper>
  );
};

export default SymptomSelector;

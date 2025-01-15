import React, { useState } from 'react';
import {
  Box,
  TextField,
  Autocomplete,
  Button,
  Typography,
  Paper,
} from '@mui/material';

interface Symptom {
  symptom_id: number;
  name: string;
  severity: number;
  notes?: string;
}

interface SymptomSelectorProps {
  selectedSymptoms: Symptom[];
  onSymptomSelect: (symptom: Symptom) => void;
  onSymptomRemove: (symptomId: number) => void;
}

const SymptomSelector: React.FC<SymptomSelectorProps> = ({
  selectedSymptoms,
  onSymptomSelect,
  onSymptomRemove,
}) => {
  const [selectedSymptomsState, setSelectedSymptomsState] = useState<Symptom[]>([]);

  const commonSymptoms = [
    { symptom_id: 1, name: 'Fever', severity: 1 },
    { symptom_id: 2, name: 'Headache', severity: 2 },
    { symptom_id: 3, name: 'Cough', severity: 3 },
    { symptom_id: 4, name: 'Fatigue', severity: 4 },
    { symptom_id: 5, name: 'Nausea', severity: 5 },
    { symptom_id: 6, name: 'Dizziness', severity: 6 },
    { symptom_id: 7, name: 'Chest Pain', severity: 7 },
    { symptom_id: 8, name: 'Shortness of Breath', severity: 8 },
    { symptom_id: 9, name: 'Body Aches', severity: 9 },
    { symptom_id: 10, name: 'Sore Throat', severity: 10 },
  ];

  const handleSubmit = async () => {
    if (selectedSymptomsState.length > 0) {
      // await onDiagnosisStart(selectedSymptomsState);
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
          value={selectedSymptomsState}
          onChange={(_, newValue) => setSelectedSymptomsState(newValue)}
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
          disabled={selectedSymptomsState.length === 0}
          fullWidth
        >
          Start Diagnosis
        </Button>
      </Box>
    </Paper>
  );
};

export default SymptomSelector;

import React, { useState, useEffect } from 'react';
import {
  Box,
  Chip,
  TextField,
  Button,
  Typography,
  Autocomplete,
  CircularProgress,
  Slider,
  Grid,
  Paper,
} from '@mui/material';
import { SymptomInput } from '../../types/diagnosis';

interface Symptom {
  id: number;
  name: string;
  description?: string;
}

interface SymptomSelectorProps {
  selectedSymptoms: SymptomInput[];
  onSymptomsChange: (symptoms: SymptomInput[]) => void;
  onSubmit: () => void;
  isSubmitting: boolean;
}

const SEVERITY_MARKS = [
  { value: 1, label: 'خفيف' },
  { value: 2, label: 'متوسط' },
  { value: 3, label: 'شديد' },
];

const commonSymptoms: Symptom[] = [
  { id: 1, name: 'حمى', description: 'ارتفاع في درجة حرارة الجسم' },
  { id: 2, name: 'سعال', description: 'سعال جاف أو مصحوب بالبلغم' },
  { id: 3, name: 'صداع', description: 'ألم في الرأس' },
  { id: 4, name: 'تعب', description: 'إرهاق وضعف عام' },
  { id: 5, name: 'ألم في العضلات', description: 'ألم وتعب في العضلات' },
];

export const SymptomSelector: React.FC<SymptomSelectorProps> = ({
  selectedSymptoms,
  onSymptomsChange,
  onSubmit,
  isSubmitting
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [availableSymptoms, setAvailableSymptoms] = useState<Symptom[]>(commonSymptoms);

  const handleSymptomAdd = (symptom: Symptom | null) => {
    if (!symptom) return;

    const newSymptom: SymptomInput = {
      symptom_id: symptom.id,
      symptom: symptom.name,
      severity: 2, // Default severity
    };

    onSymptomsChange([...selectedSymptoms, newSymptom]);
    setSearchQuery('');
  };

  const handleSymptomRemove = (symptomId: number) => {
    onSymptomsChange(selectedSymptoms.filter((s) => s.symptom_id !== symptomId));
  };

  const handleSeverityChange = (symptomId: number, newSeverity: number) => {
    onSymptomsChange(
      selectedSymptoms.map((s) =>
        s.symptom_id === symptomId ? { ...s, severity: newSeverity } : s
      )
    );
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Select Symptoms
      </Typography>

      <Autocomplete
        options={availableSymptoms.filter(
          (s) => !selectedSymptoms.some((selected) => selected.symptom_id === s.id)
        )}
        getOptionLabel={(option) => option.name}
        value={null}
        onChange={(_event, newValue) => handleSymptomAdd(newValue)}
        inputValue={searchQuery}
        onInputChange={(_event, newValue) => setSearchQuery(newValue)}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Search symptoms"
            variant="outlined"
            fullWidth
          />
        )}
      />

      <Box sx={{ mt: 3 }}>
        {selectedSymptoms.map((symptom) => (
          <Paper key={symptom.symptom_id} sx={{ p: 2, mt: 2 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={4}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Chip
                    label={symptom.symptom}
                    onDelete={() => handleSymptomRemove(symptom.symptom_id)}
                    color="primary"
                  />
                </Box>
              </Grid>

              <Grid item xs={12} sm={4}>
                <Typography gutterBottom>Severity</Typography>
                <Slider
                  value={symptom.severity}
                  min={1}
                  max={10}
                  step={1}
                  marks={[]}
                  onChange={(_event, value) =>
                    handleSeverityChange(symptom.symptom_id, value as number)
                  }
                />
              </Grid>
            </Grid>
          </Paper>
        ))}
      </Box>

      <Box sx={{ mt: 3 }}>
        <Button
          variant="contained"
          onClick={onSubmit}
          disabled={selectedSymptoms.length === 0 || isSubmitting}
          fullWidth
        >
          {isSubmitting ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            'Start Diagnosis'
          )}
        </Button>
      </Box>
    </Box>
  );
};

export default SymptomSelector;

import React, { useState } from 'react';
import {
  Box,
  TextField,
  Autocomplete,
  Chip,
  Button,
  Typography,
  CircularProgress,
} from '@mui/material';
import { SymptomInput } from '../../types/diagnosis';
import { useAIService } from '../../services/ai-service';

export interface SymptomSelectorProps {
  selectedSymptoms: SymptomInput[];
  onSymptomsChange: (symptoms: SymptomInput[]) => void;
  onSubmit: () => void;
  isSubmitting: boolean;
}

export const SymptomSelector: React.FC<SymptomSelectorProps> = ({
  selectedSymptoms,
  onSymptomsChange,
  onSubmit,
  isSubmitting,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const { getSymptoms, loading, error } = useAIService();
  const [availableSymptoms, setAvailableSymptoms] = useState<SymptomInput[]>([]);

  const handleSymptomAdd = (symptom: SymptomInput | null) => {
    if (symptom && !selectedSymptoms.some(s => s.name === symptom.name)) {
      onSymptomsChange([...selectedSymptoms, symptom]);
    }
    setSearchQuery('');
  };

  const handleSymptomRemove = (symptomToRemove: SymptomInput) => {
    onSymptomsChange(selectedSymptoms.filter(s => s.name !== symptomToRemove.name));
  };

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Autocomplete
          value={null}
          onChange={(_, newValue) => handleSymptomAdd(newValue)}
          inputValue={searchQuery}
          onInputChange={(_, newValue) => setSearchQuery(newValue)}
          options={availableSymptoms}
          getOptionLabel={(option) => option.name}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Search Symptoms"
              variant="outlined"
              fullWidth
              error={!!error}
              helperText={error}
              InputProps={{
                ...params.InputProps,
                endAdornment: (
                  <>
                    {loading && <CircularProgress size={20} />}
                    {params.InputProps.endAdornment}
                  </>
                ),
              }}
            />
          )}
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        {selectedSymptoms.length > 0 ? (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {selectedSymptoms.map((symptom) => (
              <Chip
                key={symptom.name}
                label={symptom.name}
                onDelete={() => handleSymptomRemove(symptom)}
              />
            ))}
          </Box>
        ) : (
          <Typography color="text.secondary">
            No symptoms selected. Start typing to search and add symptoms.
          </Typography>
        )}
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={onSubmit}
          disabled={selectedSymptoms.length === 0 || isSubmitting}
        >
          {isSubmitting ? (
            <>
              Analyzing...
              <CircularProgress size={20} sx={{ ml: 1 }} />
            </>
          ) : (
            'Start Diagnosis'
          )}
        </Button>
      </Box>
    </Box>
  );
};

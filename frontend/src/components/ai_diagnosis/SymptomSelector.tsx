import React, { useState, useEffect } from 'react';
import {
  Box,
  Chip,
  TextField,
  Autocomplete,
  Typography,
  Rating,
  Paper,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { useAIService } from '../../services/ai-service';

interface Symptom {
  id: number;
  name: string;
  description: string;
}

interface SelectedSymptom {
  symptom_id: number;
  name: string;
  severity: number;
  notes?: string;
}

interface SymptomSelectorProps {
  selectedSymptoms: SelectedSymptom[];
  onSymptomSelect: (symptom: SelectedSymptom) => void;
  onSymptomRemove: (symptomId: number) => void;
}

export default function SymptomSelector({
  selectedSymptoms,
  onSymptomSelect,
  onSymptomRemove,
}: SymptomSelectorProps) {
  const [symptoms, setSymptoms] = useState<Symptom[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSymptom, setSelectedSymptom] = useState<Symptom | null>(null);
  const [severity, setSeverity] = useState<number>(2);
  const [notes, setNotes] = useState('');

  const { getSymptoms } = useAIService();

  useEffect(() => {
    const loadSymptoms = async () => {
      try {
        const data = await getSymptoms();
        setSymptoms(data);
      } catch (error) {
        console.error('Error loading symptoms:', error);
      } finally {
        setLoading(false);
      }
    };

    loadSymptoms();
  }, []);

  const handleSymptomChange = (
    event: React.SyntheticEvent,
    value: Symptom | null
  ) => {
    setSelectedSymptom(value);
  };

  const handleSeverityChange = (
    event: React.SyntheticEvent,
    value: number | null
  ) => {
    setSeverity(value || 2);
  };

  const handleNotesChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setNotes(event.target.value);
  };

  const handleAddSymptom = () => {
    if (selectedSymptom) {
      onSymptomSelect({
        symptom_id: selectedSymptom.id,
        name: selectedSymptom.name,
        severity,
        notes: notes.trim(),
      });
      setSelectedSymptom(null);
      setSeverity(2);
      setNotes('');
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          إضافة الأعراض
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
          <Autocomplete
            sx={{ flex: 1 }}
            options={symptoms}
            loading={loading}
            value={selectedSymptom}
            onChange={handleSymptomChange}
            getOptionLabel={(option) => option.name}
            renderInput={(params) => (
              <TextField
                {...params}
                label="اختر العرض"
                variant="outlined"
              />
            )}
            renderOption={(props, option) => (
              <li {...props}>
                <Typography noWrap>
                  {option.name}
                </Typography>
              </li>
            )}
          />

          <Box sx={{ minWidth: 200 }}>
            <Typography component="legend">شدة العرض</Typography>
            <Rating
              value={severity}
              onChange={handleSeverityChange}
              max={3}
            />
          </Box>
        </Box>

        <TextField
          fullWidth
          multiline
          rows={2}
          variant="outlined"
          label="ملاحظات إضافية"
          value={notes}
          onChange={handleNotesChange}
          sx={{ mt: 2 }}
        />
      </Box>

      <Paper variant="outlined" sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          الأعراض المختارة
        </Typography>

        {selectedSymptoms.length === 0 ? (
          <Typography color="text.secondary">
            لم يتم اختيار أي أعراض بعد
          </Typography>
        ) : (
          <List>
            {selectedSymptoms.map((symptom) => (
              <ListItem key={symptom.symptom_id}>
                <ListItemText
                  primary={symptom.name}
                  secondary={
                    <>
                      <Rating
                        value={symptom.severity}
                        readOnly
                        max={3}
                        size="small"
                      />
                      {symptom.notes && (
                        <Typography variant="body2" sx={{ mt: 1 }}>
                          {symptom.notes}
                        </Typography>
                      )}
                    </>
                  }
                />
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    onClick={() => onSymptomRemove(symptom.symptom_id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
    </Box>
  );
}

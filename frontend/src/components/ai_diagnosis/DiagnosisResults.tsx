import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
  Grid,
} from '@mui/material';
import { DiagnosisResult } from '../../types/diagnosis';

interface DiagnosisResultsProps {
  result: DiagnosisResult;
}

const getRiskColor = (riskLevel: 'low' | 'medium' | 'high'): string => {
  switch (riskLevel) {
    case 'high':
      return '#f44336';
    case 'medium':
      return '#ff9800';
    case 'low':
      return '#4caf50';
    default:
      return '#757575';
  }
};

export const DiagnosisResults: React.FC<DiagnosisResultsProps> = ({ result }) => {
  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        Diagnosis Results
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              Primary Diagnosis:
            </Typography>
            <Typography variant="h6" color="primary">
              {result.diagnosis}
            </Typography>
          </Box>

          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              Risk Level:
            </Typography>
            <Chip
              label={result.riskLevel.toUpperCase()}
              sx={{
                bgcolor: getRiskColor(result.riskLevel),
                color: 'white',
                fontWeight: 'bold',
              }}
            />
          </Box>

          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              Confidence Score:
            </Typography>
            <Typography>
              {Math.round(result.confidence * 100)}%
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography variant="subtitle1" gutterBottom>
            Reported Symptoms:
          </Typography>
          <List dense>
            {result.symptoms.map((symptom, index) => (
              <ListItem key={index}>
                <ListItemText primary={symptom} />
              </ListItem>
            ))}
          </List>
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography variant="subtitle1" gutterBottom>
            Recommendations:
          </Typography>
          <List dense>
            {result.recommendations.map((recommendation, index) => (
              <ListItem key={index}>
                <ListItemText primary={recommendation} />
              </ListItem>
            ))}
          </List>
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      <Box sx={{ mt: 2 }}>
        <Typography variant="caption" color="text.secondary">
          Diagnosis ID: {result.id}
          <br />
          Generated on: {new Date(result.timestamp).toLocaleString()}
          {result.doctorId && (
            <>
              <br />
              Reviewed by Doctor ID: {result.doctorId}
            </>
          )}
        </Typography>
      </Box>
    </Paper>
  );
};

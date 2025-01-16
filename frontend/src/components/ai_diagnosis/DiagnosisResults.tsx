import React from 'react';
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  Grid,
  useTheme,
} from '@mui/material';
import {
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { DiagnosisResult } from '../../types/diagnosis';

interface DiagnosisResultsProps {
  results: DiagnosisResult[];
}

export function DiagnosisResults({ results }: DiagnosisResultsProps) {
  const theme = useTheme();

  const getRiskLevelColor = (riskLevel: DiagnosisResult['riskLevel']) => {
    switch (riskLevel) {
      case 'high':
        return theme.palette.error.main;
      case 'medium':
        return theme.palette.warning.main;
      case 'low':
        return theme.palette.success.main;
      default:
        return theme.palette.info.main;
    }
  };

  const getRiskLevelIcon = (riskLevel: DiagnosisResult['riskLevel']) => {
    switch (riskLevel) {
      case 'high':
        return <ErrorIcon />;
      case 'medium':
        return <WarningIcon />;
      case 'low':
        return <InfoIcon />;
      default:
        return <InfoIcon />;
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Diagnosis Results
      </Typography>

      {results.map((result) => (
        <Paper key={result.id} sx={{ p: 3, mb: 3 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <Typography variant="h6">{result.diagnosis}</Typography>
                <Chip
                  icon={getRiskLevelIcon(result.riskLevel)}
                  label={`Risk Level: ${result.riskLevel}`}
                  sx={{
                    bgcolor: getRiskLevelColor(result.riskLevel),
                    color: 'white',
                  }}
                />
                <Chip
                  label={`Confidence: ${Math.round(result.confidence * 100)}%`}
                  color="primary"
                  variant="outlined"
                />
              </Box>
            </Grid>

            {result.details?.matching_symptoms && (
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" gutterBottom>
                  Matching Symptoms
                </Typography>
                <List dense>
                  {result.details.matching_symptoms.map((symptom, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={symptom.name}
                        secondary={`Importance: ${symptom.importance}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </Grid>
            )}

            {result.details?.missing_symptoms && (
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" gutterBottom>
                  Missing Symptoms
                </Typography>
                <List dense>
                  {result.details.missing_symptoms.map((symptom, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={symptom.name}
                        secondary={`Importance: ${symptom.importance}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </Grid>
            )}

            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom>
                Recommendations
              </Typography>
              <List dense>
                {result.recommendations.map((recommendation, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={recommendation} />
                  </ListItem>
                ))}
              </List>
            </Grid>

            {result.details?.icd_code && (
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">
                  ICD Code: {result.details.icd_code}
                </Typography>
              </Grid>
            )}
          </Grid>
        </Paper>
      ))}
    </Box>
  );
}

export default DiagnosisResults;

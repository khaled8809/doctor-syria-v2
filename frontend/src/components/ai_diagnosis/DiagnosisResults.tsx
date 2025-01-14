import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Button,
  Grid,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import InfoIcon from '@mui/icons-material/Info';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import AssignmentIcon from '@mui/icons-material/Assignment';
import { PDFDownloadButton } from '../common/PDFDownloadButton';

interface DiagnosisResult {
  disease: {
    name: string;
    icd_code: string;
    risk_level: number;
  };
  confidence: number;
  reasoning: {
    matching_symptoms: Array<{
      name: string;
      importance: number;
    }>;
    missing_symptoms: Array<{
      name: string;
      importance: number;
    }>;
    confidence_explanation: string;
  };
  recommendations: string;
}

interface DiagnosisResultsProps {
  results: DiagnosisResult[];
}

export default function DiagnosisResults({ results }: DiagnosisResultsProps) {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return 'success';
    if (confidence >= 50) return 'warning';
    return 'error';
  };

  const getRiskLevelInfo = (level: number) => {
    switch (level) {
      case 3:
        return { color: 'error', label: 'خطر مرتفع', icon: <WarningIcon /> };
      case 2:
        return { color: 'warning', label: 'خطر متوسط', icon: <InfoIcon /> };
      default:
        return { color: 'success', label: 'خطر منخفض', icon: <CheckCircleIcon /> };
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h5" gutterBottom>
          نتائج التشخيص
        </Typography>
        <PDFDownloadButton
          content={results}
          fileName="diagnosis-results"
        />
      </Box>

      <Grid container spacing={3}>
        {results.map((result, index) => (
          <Grid item xs={12} key={index}>
            <Card variant="outlined">
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6" component="div">
                    {result.disease.name}
                  </Typography>
                  <Box>
                    <Chip
                      label={`${result.confidence}% ثقة`}
                      color={getConfidenceColor(result.confidence)}
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={result.disease.icd_code}
                      variant="outlined"
                    />
                  </Box>
                </Box>

                <Box sx={{ mb: 3 }}>
                  {result.reasoning.matching_symptoms.length > 0 && (
                    <>
                      <Typography variant="subtitle1" gutterBottom>
                        الأعراض المطابقة:
                      </Typography>
                      <List dense>
                        {result.reasoning.matching_symptoms.map((symptom, idx) => (
                          <ListItem key={idx}>
                            <ListItemIcon>
                              <CheckCircleIcon color="success" />
                            </ListItemIcon>
                            <ListItemText
                              primary={symptom.name}
                              secondary={`درجة الأهمية: ${symptom.importance}`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}

                  {result.reasoning.missing_symptoms.length > 0 && (
                    <>
                      <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                        الأعراض غير الموجودة:
                      </Typography>
                      <List dense>
                        {result.reasoning.missing_symptoms.map((symptom, idx) => (
                          <ListItem key={idx}>
                            <ListItemIcon>
                              <InfoIcon color="info" />
                            </ListItemIcon>
                            <ListItemText
                              primary={symptom.name}
                              secondary={`درجة الأهمية: ${symptom.importance}`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}
                </Box>

                <Divider sx={{ my: 2 }} />

                <Typography variant="subtitle1" gutterBottom>
                  التوصيات:
                </Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ whiteSpace: 'pre-line' }}
                >
                  {result.recommendations}
                </Typography>

                <Box sx={{ mt: 3, display: 'flex', gap: 1 }}>
                  <Button
                    variant="contained"
                    startIcon={<LocalHospitalIcon />}
                    color="primary"
                  >
                    إنشاء وصفة طبية
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<AssignmentIcon />}
                  >
                    إضافة إلى السجل الطبي
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

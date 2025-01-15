import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';

interface DiagnosisResult {
  id: string;
  diagnosis: string;
  confidence: number;
  recommendations: string[];
  riskLevel: 'low' | 'medium' | 'high';
}

interface DiagnosisResultsProps {
  results: DiagnosisResult;
}

const getRiskLevelColor = (level: string) => {
  switch (level) {
    case 'high':
      return 'error';
    case 'medium':
      return 'warning';
    default:
      return 'success';
  }
};

const DiagnosisResults: React.FC<DiagnosisResultsProps> = ({ results }) => {
  return (
    <Box>
      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h6">التشخيص المقترح</Typography>
            <Chip
              label={`${Math.round(results.confidence * 100)}% نسبة الثقة`}
              color="primary"
              variant="outlined"
            />
          </Box>
          <Typography variant="h5" gutterBottom>
            {results.diagnosis}
          </Typography>
          <Chip
            label={results.riskLevel === 'high' ? 'خطر مرتفع' : results.riskLevel === 'medium' ? 'خطر متوسط' : 'خطر منخفض'}
            color={getRiskLevelColor(results.riskLevel)}
            sx={{ mt: 1 }}
          />
        </CardContent>
      </Card>

      <Card elevation={2}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            التوصيات والإجراءات المقترحة
          </Typography>
          <List>
            {results.recommendations.map((recommendation, index) => (
              <ListItem key={index}>
                <ListItemText primary={recommendation} />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DiagnosisResults;

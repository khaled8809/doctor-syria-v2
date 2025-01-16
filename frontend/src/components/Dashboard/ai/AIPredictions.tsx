import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  LinearProgress
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Warning,
  Info,
  Psychology,
  Analytics
} from '@mui/icons-material';

interface Prediction {
  id: string;
  type: string;
  prediction: string;
  confidence: number;
  actions: string[];
}

interface AIPredictionsProps {
  predictions: Prediction[];
  onPredictionAction: (predictionId: string, action: string) => void;
}

export const AIPredictions: React.FC<AIPredictionsProps> = ({ predictions, onPredictionAction }) => {
  return (
    <Paper sx={{ p: 2, height: '100%' }}>
      <Box display="flex" alignItems="center" mb={2}>
        <Psychology sx={{ mr: 1 }} />
        <Typography variant="h6">AI Predictions & Insights</Typography>
      </Box>

      <Grid container spacing={2}>
        {predictions.map((prediction) => (
          <Grid item xs={12} key={prediction.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {prediction.type}
                  </Typography>
                  <Chip
                    icon={prediction.confidence >= 0.7 ? <TrendingUp /> : <Warning />}
                    label={`${(prediction.confidence * 100).toFixed(0)}% Confidence`}
                    color={prediction.confidence >= 0.7 ? "success" : "warning"}
                    size="small"
                  />
                </Box>

                <Typography color="text.secondary" mb={2}>
                  {prediction.prediction}
                </Typography>

                <LinearProgress
                  variant="determinate"
                  value={prediction.confidence * 100}
                  sx={{ mb: 2 }}
                />

                <Box display="flex" gap={1} flexWrap="wrap">
                  {prediction.actions.map((action, index) => (
                    <Button
                      key={index}
                      size="small"
                      variant="outlined"
                      onClick={() => onPredictionAction(prediction.id, action)}
                    >
                      {action}
                    </Button>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
};

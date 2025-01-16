import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  LinearProgress,
  Chip
} from '@mui/material';
import { Warning } from '@mui/icons-material';

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

export const AIPredictions: React.FC<AIPredictionsProps> = ({
  predictions,
  onPredictionAction
}) => {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
          <Warning color="warning" sx={{ mr: 1 }} />
          <Typography variant="h6" component="div">
            AI Predictions & Insights
          </Typography>
        </Box>
        <Grid container spacing={2}>
          {predictions.map((prediction) => (
            <Grid item xs={12} key={prediction.id}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    {prediction.type}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" gutterBottom>
                    {prediction.prediction}
                  </Typography>
                  <Box sx={{ mt: 2, mb: 1 }}>
                    <Typography variant="body2" color="text.secondary">
                      Confidence: {(prediction.confidence * 100).toFixed(0)}%
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={prediction.confidence * 100}
                      color={getConfidenceColor(prediction.confidence)}
                      sx={{ mt: 1 }}
                    />
                  </Box>
                  <Box sx={{ mt: 2 }}>
                    {prediction.actions.map((action) => (
                      <Chip
                        key={action}
                        label={action}
                        onClick={() => onPredictionAction(prediction.id, action)}
                        sx={{ mr: 1, mb: 1 }}
                        clickable
                      />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
};

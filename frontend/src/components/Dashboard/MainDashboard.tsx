import React from 'react';
import { Box, Container, Grid } from '@mui/material';
import { AIPredictions } from './ai/AIPredictions';
import { AdvancedAnalytics } from './analytics/AdvancedAnalytics';
import { Analytics } from '../../types/analytics';

interface Props {
  data: Analytics;
}

export const MainDashboard: React.FC<Props> = ({ data }) => {
  const mockPredictions = [
    {
      id: '1',
      type: 'Patient Risk',
      prediction: 'High risk of readmission',
      confidence: 0.85,
      actions: ['Schedule follow-up', 'Review medication']
    },
    {
      id: '2',
      type: 'Resource Allocation',
      prediction: 'Bed shortage expected',
      confidence: 0.78,
      actions: ['Optimize discharge process', 'Alert management']
    }
  ];

  const handlePredictionAction = (predictionId: string, action: string) => {
    console.log(`Action ${action} taken for prediction ${predictionId}`);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box sx={{ mb: 2 }}>
            <AIPredictions
              predictions={mockPredictions}
              onPredictionAction={handlePredictionAction}
            />
          </Box>
        </Grid>
        <Grid item xs={12}>
          <AdvancedAnalytics analytics={data} />
        </Grid>
      </Grid>
    </Container>
  );
};

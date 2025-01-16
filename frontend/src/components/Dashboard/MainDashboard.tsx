import React from 'react';
import { Box, Container, Grid } from '@mui/material';
import { Analytics } from '../../types/analytics';
import { AIPredictions } from './ai/AIPredictions';
import { SmartAlertSystem } from './alerts/SmartAlertSystem';
import { AdvancedAnalytics } from './analytics/AdvancedAnalytics';
import { ResourceManagement } from './resources/ResourceManagement';
import { TaskManagement } from './tasks/TaskManagement';
import { Notification, Task, Resource } from '../../types/common';

interface MainDashboardProps {
  updateState?: (newState: any) => void;
}

interface AnalyticsProps {
  data: Analytics;
}

const defaultAnalytics: Analytics = {
  predictions: {
    patientLoad: [],
    resourceNeeds: [],
    staffingRequirements: []
  },
  departmentPerformance: {
    efficiency: 0,
    satisfaction: 0,
    waitTimes: 0
  },
  resourceUtilization: {
    beds: 0,
    equipment: 0,
    staff: 0
  },
  financialMetrics: {
    revenue: 0,
    expenses: 0,
    profit: 0
  }
};

export const MainDashboard: React.FC<MainDashboardProps> = () => {
  const notifications: Notification[] = [];
  const tasks: Task[] = [];
  const resources: Resource[] = [];
  const predictions = [
    { id: '1', type: 'diagnosis', prediction: 'High risk of condition A', confidence: 0.85, actions: ['Refer to specialist', 'Order tests'] },
  ];

  const handleAlertAction = (alertId: string, action: string) => {
    console.log(`Alert ${alertId} action: ${action}`);
  };

  const handleTaskUpdate = async (taskId: string, updates: any) => {
    try {
      console.log(`Task ${taskId} updates: ${JSON.stringify(updates)}`);
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handlePredictionAction = (predictionId: string, action: string) => {
    console.log(`Prediction ${predictionId} action: ${action}`);
  };

  return (
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        py: 8
      }}
    >
      <Container maxWidth="xl">
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={4}>
            <AIPredictions data={defaultAnalytics} predictions={predictions} onPredictionAction={handlePredictionAction} />
          </Grid>
          <Grid item xs={12} md={6} lg={4}>
            <SmartAlertSystem alerts={notifications} onAlertAction={handleAlertAction} />
          </Grid>
          <Grid item xs={12} lg={4}>
            <AdvancedAnalytics data={defaultAnalytics} />
          </Grid>
          <Grid item xs={12} md={6}>
            <ResourceManagement resources={resources} />
          </Grid>
          <Grid item xs={12} md={6}>
            <TaskManagement tasks={tasks} onTaskUpdate={handleTaskUpdate} />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

import React from 'react';
import { Box, Grid } from '@mui/material';
import { SmartAlertSystem } from './alerts/SmartAlertSystem';
import { TaskManagement } from './tasks/TaskManagement';
import { ResourceManagement } from './resources/ResourceManagement';
import { AIPredictions } from './ai/AIPredictions';
import { AdvancedAnalytics } from './analytics/AdvancedAnalytics';
import { Notification, Task, Resource } from '../../types/common';

interface MainDashboardProps {
  updateState?: (newState: any) => void;
}

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
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <SmartAlertSystem
            alerts={notifications}
            onAlertAction={handleAlertAction}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TaskManagement
            tasks={tasks}
            onTaskUpdate={handleTaskUpdate}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <ResourceManagement
            resources={resources}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <AIPredictions
            predictions={predictions}
            onPredictionAction={handlePredictionAction}
          />
        </Grid>

        <Grid item xs={12}>
          <AdvancedAnalytics />
        </Grid>
      </Grid>
    </Box>
  );
};

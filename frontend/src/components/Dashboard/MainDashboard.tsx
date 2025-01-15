import React from 'react';
import { Box, Grid } from '@mui/material';
import { SmartAlertSystem } from './alerts/SmartAlertSystem';
import { TaskManagement } from './tasks/TaskManagement';
import { ResourceManagement } from './resources/ResourceManagement';
import { AIPredictions } from './ai/AIPredictions';
import { AdvancedAnalytics } from './analytics/AdvancedAnalytics';
import { useAppSelector } from '../../store';

interface MainDashboardProps {
  updateState?: (newState: any) => void;
}

export const MainDashboard: React.FC<MainDashboardProps> = () => {
  const notifications: Notification[] = [];
  const tasks: Task[] = [];
  const employees: User[] = [];
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

  const handleResourceUpdate = async (resourceId: string, updates: any) => {
    try {
      console.log(`Resource ${resourceId} updates: ${JSON.stringify(updates)}`);
    } catch (error) {
      console.error('Error updating resource:', error);
    }
  };

  const handlePredictionAction = (predictionId: string, action: string) => {
    console.log(`Prediction ${predictionId} action: ${action}`);
  };

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <SmartAlertSystem 
            alerts={notifications} 
            onAlertAction={handleAlertAction} 
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TaskManagement 
            tasks={tasks} 
            employees={employees} 
            onTaskUpdate={handleTaskUpdate} 
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <ResourceManagement 
            resources={resources} 
            onResourceUpdate={handleResourceUpdate} 
          />
        </Grid>
        <Grid item xs={12}>
          <AIPredictions 
            predictions={predictions} 
            onPredictionAction={handlePredictionAction} 
          />
        </Grid>
        <Grid item xs={12}>
          <AdvancedAnalytics 
            patientStats={{
              total: 1000,
              admitted: 150,
              discharged: 100,
              critical: 20
            }}
            financialStats={{
              revenue: 500000,
              expenses: 300000,
              profit: 200000,
              trend: 'up'
            }}
          />
        </Grid>
      </Grid>
    </Box>
  );
};

import React from 'react';
import { Box, Grid, Paper, useTheme } from '@mui/material';
import { DashboardProvider, useDashboard } from './integration/DashboardIntegration';
import { SmartTaskSystem } from './tasks/SmartTaskSystem';
import { AdvancedResourceManagement } from './resources/AdvancedResourceManagement';
import { AIPredictions } from './ai/AIPredictions';
import { SmartAlertSystem } from './alerts/SmartAlertSystem';
import { AdvancedAnalytics } from './analytics/AdvancedAnalytics';
import { AdvancedReporting } from './reports/AdvancedReporting';

// مكون لوحة التحكم الداخلية
const DashboardContent: React.FC = () => {
  const { state, updateState, refreshData } = useDashboard();
  const theme = useTheme();

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Grid container spacing={3}>
        {/* نظام التنبيهات الذكي */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <SmartAlertSystem
              alerts={state.notifications}
              onAlertAction={(alertId, action) => {
                // معالجة إجراءات التنبيهات
              }}
            />
          </Paper>
        </Grid>

        {/* نظام المهام الذكي */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <SmartTaskSystem
              tasks={state.tasks}
              employees={state.currentUser ? [state.currentUser] : []}
              onTaskUpdate={async (taskId, updates) => {
                try {
                  await updateTask(taskId, updates);
                  await refreshData();
                } catch (error) {
                  console.error('Failed to update task:', error);
                }
              }}
            />
          </Paper>
        </Grid>

        {/* إدارة الموارد المتقدمة */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <AdvancedResourceManagement
              resources={state.resources}
              onResourceUpdate={async (resourceId, updates) => {
                try {
                  await updateResource(resourceId, updates);
                  await refreshData();
                } catch (error) {
                  console.error('Failed to update resource:', error);
                }
              }}
            />
          </Paper>
        </Grid>

        {/* التنبؤات الذكية */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <AIPredictions
              predictions={state.analytics?.predictions || []}
              onPredictionAction={(predictionId, action) => {
                // معالجة إجراءات التنبؤات
              }}
            />
          </Paper>
        </Grid>

        {/* التحليلات المتقدمة */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <AdvancedAnalytics
              data={{
                patientMetrics: state.analytics?.patientMetrics || [],
                departmentPerformance: state.analytics?.departmentPerformance || [],
                resourceUtilization: state.analytics?.resourceUtilization || [],
                financialMetrics: state.analytics?.financialMetrics || []
              }}
            />
          </Paper>
        </Grid>

        {/* نظام التقارير */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <AdvancedReporting />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

// مكون لوحة التحكم الرئيسية مع مزود السياق
export const MainDashboard: React.FC = () => {
  return (
    <DashboardProvider>
      <DashboardContent />
    </DashboardProvider>
  );
};

export default MainDashboard;

import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
  Alert,
  useTheme,
} from '@mui/material';
import { usePatientContext } from '../../contexts/PatientContext';
import { useAIService } from '../../services/ai-service';
import { HealthRisk, HealthMetric } from '../../types/diagnosis';

interface HealthRiskPredictorProps {
  risk: HealthRisk;
  metrics: HealthMetric[];
}

const getRiskColor = (level: string): string => {
  switch (level) {
    case 'high':
      return '#f44336';
    case 'medium':
      return '#ff9800';
    case 'low':
      return '#4caf50';
    default:
      return '#757575';
  }
};

const getMetricColor = (status: HealthMetric['status']) => {
  switch (status) {
    case 'critical':
      return '#f44336';
    case 'warning':
      return '#ff9800';
    case 'normal':
      return '#4caf50';
    default:
      return '#757575';
  }
};

export function HealthRiskPredictor() {
  const theme = useTheme();
  const { currentPatient } = usePatientContext();
  const { predictHealthRisks, getHealthMetrics } = useAIService();

  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [healthRisks, setHealthRisks] = React.useState<HealthRisk[]>([]);
  const [healthMetrics, setHealthMetrics] = React.useState<HealthMetric[]>([]);

  React.useEffect(() => {
    if (!currentPatient) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [risks, metrics] = await Promise.all([
          predictHealthRisks(currentPatient.id),
          getHealthMetrics(currentPatient.id),
        ]);

        setHealthRisks(risks);
        setHealthMetrics(metrics);
      } catch (err) {
        setError('حدث خطأ أثناء تحليل المخاطر الصحية');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPatient, predictHealthRisks, getHealthMetrics]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        تحليل المخاطر الصحية
      </Typography>

      <Grid container spacing={3}>
        {healthRisks.map((risk, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                {risk.riskType}
              </Typography>

              <Box sx={{ mb: 2 }}>
                <Chip
                  label={`Risk Level: ${risk.riskLevel.toUpperCase()}`}
                  sx={{
                    bgcolor: getRiskColor(risk.riskLevel),
                    color: 'white',
                    fontWeight: 'bold',
                  }}
                />
              </Box>

              <Typography variant="body1" gutterBottom>
                {risk.description}
              </Typography>

              <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
                Key Metrics:
              </Typography>
              <List dense>
                {healthMetrics
                  .filter((metric) => metric.name === risk.riskType)
                  .map((metric, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={`${metric.name}: ${metric.value}${metric.unit}`}
                        secondary={`Normal Range: ${metric.normalRange.min}-${metric.normalRange.max}${metric.unit}`}
                      />
                    </ListItem>
                  ))}
              </List>

              <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
                Recommendations:
              </Typography>
              <List dense>
                {risk.recommendations.map((recommendation, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={recommendation} />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default HealthRiskPredictor;

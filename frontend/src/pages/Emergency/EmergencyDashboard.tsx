import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
  IconButton,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Warning,
  LocalHospital,
  DirectionsRun,
  Timer,
  Message,
  Phone,
  VideoCall,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format } from 'date-fns';

interface EmergencyCase {
  id: number;
  patient_name: string;
  condition: string;
  priority: 'critical' | 'urgent' | 'stable';
  arrival_time: string;
  status: 'waiting' | 'in_treatment' | 'transferred' | 'discharged';
  assigned_doctor?: string;
  assigned_room?: string;
  vital_signs?: {
    blood_pressure: string;
    heart_rate: number;
    temperature: number;
    oxygen_saturation: number;
  };
  notes: string;
}

const EmergencyDashboard = () => {
  const [selectedCase, setSelectedCase] = useState<EmergencyCase | null>(null);
  const [newCaseDialog, setNewCaseDialog] = useState(false);
  const [communicationDialog, setCommunicationDialog] = useState(false);
  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();

  // Fetch emergency cases
  const { data: emergencyCases, isLoading } = useQuery<EmergencyCase[]>(
    'emergency-cases',
    () => axios.get('/api/emergency/cases/').then((res) => res.data)
  );

  // Add new emergency case
  const addCaseMutation = useMutation(
    (newCase: Partial<EmergencyCase>) =>
      axios.post('/api/emergency/cases/', newCase),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('emergency-cases');
        enqueueSnackbar('Emergency case added successfully', {
          variant: 'success',
        });
        setNewCaseDialog(false);
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error adding case', {
          variant: 'error',
        });
      },
    }
  );

  // Update emergency case
  const updateCaseMutation = useMutation(
    (data: { id: number; updates: Partial<EmergencyCase> }) =>
      axios.patch(`/api/emergency/cases/${data.id}/`, data.updates),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('emergency-cases');
        enqueueSnackbar('Case updated successfully', { variant: 'success' });
      },
    }
  );

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'error';
      case 'urgent':
        return 'warning';
      case 'stable':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'waiting':
        return 'error';
      case 'in_treatment':
        return 'warning';
      case 'transferred':
        return 'info';
      case 'discharged':
        return 'success';
      default:
        return 'default';
    }
  };

  const handleStartTreatment = (caseId: number) => {
    updateCaseMutation.mutate({
      id: caseId,
      updates: { status: 'in_treatment' },
    });
  };

  const handleTransferCase = (caseId: number) => {
    // Open transfer dialog
    setCommunicationDialog(true);
    setSelectedCase(
      emergencyCases?.find((case_) => case_.id === caseId) || null
    );
  };

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="400px"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">Emergency Dashboard</Typography>
            <Button
              variant="contained"
              color="error"
              startIcon={<Warning />}
              onClick={() => setNewCaseDialog(true)}
            >
              New Emergency Case
            </Button>
          </Box>
        </Grid>

        {/* Stats Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Critical Cases
              </Typography>
              <Typography variant="h4">
                {
                  emergencyCases?.filter(
                    (case_) => case_.priority === 'critical'
                  ).length
                }
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Waiting for Treatment
              </Typography>
              <Typography variant="h4">
                {
                  emergencyCases?.filter((case_) => case_.status === 'waiting')
                    .length
                }
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                In Treatment
              </Typography>
              <Typography variant="h4">
                {
                  emergencyCases?.filter(
                    (case_) => case_.status === 'in_treatment'
                  ).length
                }
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Wait Time
              </Typography>
              <Typography variant="h4">12 min</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Emergency Cases List */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Active Emergency Cases
            </Typography>
            <List>
              {emergencyCases
                ?.filter((case_) => case_.status !== 'discharged')
                .map((case_) => (
                  <ListItem
                    key={case_.id}
                    divider
                    sx={{
                      backgroundColor:
                        case_.priority === 'critical'
                          ? 'error.main'
                          : 'transparent',
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle1">
                            {case_.patient_name}
                          </Typography>
                          <Chip
                            size="small"
                            label={case_.priority}
                            color={getPriorityColor(case_.priority) as any}
                          />
                          <Chip
                            size="small"
                            label={case_.status}
                            color={getStatusColor(case_.status) as any}
                          />
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="body2">
                            Condition: {case_.condition}
                          </Typography>
                          <Typography variant="body2">
                            Arrival:{' '}
                            {format(
                              new Date(case_.arrival_time),
                              'MMM d, HH:mm'
                            )}
                          </Typography>
                          {case_.vital_signs && (
                            <Typography variant="body2">
                              BP: {case_.vital_signs.blood_pressure} | HR:{' '}
                              {case_.vital_signs.heart_rate} | Temp:{' '}
                              {case_.vital_signs.temperature}°C | O2:{' '}
                              {case_.vital_signs.oxygen_saturation}%
                            </Typography>
                          )}
                        </>
                      }
                    />
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        onClick={() => handleTransferCase(case_.id)}
                      >
                        <Message />
                      </IconButton>
                      <IconButton edge="end">
                        <Phone />
                      </IconButton>
                      <IconButton edge="end">
                        <VideoCall />
                      </IconButton>
                      {case_.status === 'waiting' && (
                        <Button
                          variant="contained"
                          color="primary"
                          startIcon={<DirectionsRun />}
                          onClick={() => handleStartTreatment(case_.id)}
                          sx={{ ml: 1 }}
                        >
                          Start Treatment
                        </Button>
                      )}
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* New Case Dialog */}
      <Dialog
        open={newCaseDialog}
        onClose={() => setNewCaseDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>New Emergency Case</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Patient Name"
                variant="outlined"
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Condition"
                multiline
                rows={3}
                variant="outlined"
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Priority"
                select
                SelectProps={{
                  native: true,
                }}
                variant="outlined"
                required
              >
                <option value="critical">Critical</option>
                <option value="urgent">Urgent</option>
                <option value="stable">Stable</option>
              </TextField>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewCaseDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="primary"
            disabled={addCaseMutation.isLoading}
          >
            {addCaseMutation.isLoading ? (
              <CircularProgress size={24} />
            ) : (
              'Add Case'
            )}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Communication Dialog */}
      <Dialog
        open={communicationDialog}
        onClose={() => setCommunicationDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Emergency Communication</DialogTitle>
        <DialogContent>
          {selectedCase && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <Alert severity="error">
                  Critical Case: {selectedCase.patient_name}
                </Alert>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1">Available Actions:</Typography>
                <List>
                  <ListItem>
                    <ListItemText primary="Start Video Conference" />
                    <Button
                      variant="contained"
                      startIcon={<VideoCall />}
                      onClick={() => {
                        // Start video conference
                      }}
                    >
                      Start
                    </Button>
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Request Transfer" />
                    <Button
                      variant="contained"
                      color="warning"
                      startIcon={<LocalHospital />}
                      onClick={() => {
                        // Request transfer
                      }}
                    >
                      Request
                    </Button>
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Send Alert to All Hospitals" />
                    <Button
                      variant="contained"
                      color="error"
                      startIcon={<Warning />}
                      onClick={() => {
                        // Send alert
                      }}
                    >
                      Alert
                    </Button>
                  </ListItem>
                </List>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCommunicationDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default EmergencyDashboard;

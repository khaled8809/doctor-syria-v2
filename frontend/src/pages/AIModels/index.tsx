import { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PlayArrow as StartIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  Science as ScienceIcon,
  Assessment as AssessmentIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const modelTypes = [
  { value: 'DIAGNOSIS', label: 'Diagnosis Prediction' },
  { value: 'RISK', label: 'Risk Assessment' },
  { value: 'TREATMENT', label: 'Treatment Recommendation' },
  { value: 'IMAGE', label: 'Image Analysis' },
];

interface AIModel {
  id: number;
  name: string;
  type: string;
  status: string;
  accuracy: number;
  last_trained: string;
  predictions_count: number;
  performance_metrics: {
    precision: number;
    recall: number;
    f1_score: number;
  };
}

export default function AIModels() {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedModel, setSelectedModel] = useState<AIModel | null>(null);
  const [openMetricsDialog, setOpenMetricsDialog] = useState(false);
  const queryClient = useQueryClient();

  const { data: models, isLoading } = useQuery('ai-models', () =>
    axios.get('/api/ai-models/').then((res) => res.data)
  );

  const addModelMutation = useMutation(
    (newModel: Partial<AIModel>) => axios.post('/api/ai-models/', newModel),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('ai-models');
        setOpenDialog(false);
      },
    }
  );

  const updateModelMutation = useMutation(
    (updatedModel: Partial<AIModel>) =>
      axios.put(`/api/ai-models/${selectedModel?.id}/`, updatedModel),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('ai-models');
        setOpenDialog(false);
      },
    }
  );

  const trainModelMutation = useMutation(
    (modelId: number) => axios.post(`/api/ai-models/${modelId}/train/`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('ai-models');
      },
    }
  );

  const handleAddModel = () => {
    setSelectedModel(null);
    setOpenDialog(true);
  };

  const handleEditModel = (model: AIModel) => {
    setSelectedModel(model);
    setOpenDialog(true);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);
    const modelData = Object.fromEntries(formData.entries());

    if (selectedModel) {
      updateModelMutation.mutate(modelData);
    } else {
      addModelMutation.mutate(modelData);
    }
  };

  const getStatusChip = (status: string) => {
    const statusColors: { [key: string]: 'success' | 'error' | 'warning' | 'default' } = {
      ACTIVE: 'success',
      TRAINING: 'warning',
      INACTIVE: 'error',
      FAILED: 'error',
    };

    return (
      <Chip
        label={status}
        color={statusColors[status] || 'default'}
        size="small"
      />
    );
  };

  const getAccuracyColor = (accuracy: number) => {
    if (accuracy >= 90) return 'success';
    if (accuracy >= 70) return 'warning';
    return 'error';
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">AI Models</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddModel}
        >
          Add Model
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="h6">Model List</Typography>
                <IconButton onClick={() => queryClient.invalidateQueries('ai-models')}>
                  <RefreshIcon />
                </IconButton>
              </Box>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Accuracy</TableCell>
                      <TableCell>Last Trained</TableCell>
                      <TableCell>Predictions</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {models?.map((model: AIModel) => (
                      <TableRow key={model.id}>
                        <TableCell>{model.name}</TableCell>
                        <TableCell>{model.type}</TableCell>
                        <TableCell>{getStatusChip(model.status)}</TableCell>
                        <TableCell>
                          <Chip
                            label={`${model.accuracy}%`}
                            color={getAccuracyColor(model.accuracy)}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(model.last_trained).toLocaleDateString()}
                        </TableCell>
                        <TableCell>{model.predictions_count}</TableCell>
                        <TableCell>
                          <IconButton
                            size="small"
                            onClick={() => trainModelMutation.mutate(model.id)}
                          >
                            {model.status === 'ACTIVE' ? <StopIcon /> : <StartIcon />}
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleEditModel(model)}
                          >
                            <EditIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => setOpenMetricsDialog(true)}
                          >
                            <AssessmentIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Performance Overview
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Average Accuracy
                </Typography>
                <Box display="flex" alignItems="center" gap={1}>
                  <LinearProgress
                    variant="determinate"
                    value={85}
                    sx={{ flexGrow: 1 }}
                  />
                  <Typography variant="body2">85%</Typography>
                </Box>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Total Predictions
                </Typography>
                <Typography variant="h4">12,345</Typography>
              </Box>
              <Box sx={{ height: 200 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={models}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="accuracy"
                      stroke="#8884d8"
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedModel ? 'Edit Model' : 'Add New Model'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Model Name"
                  name="name"
                  defaultValue={selectedModel?.name}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth required>
                  <InputLabel>Model Type</InputLabel>
                  <Select
                    name="type"
                    defaultValue={selectedModel?.type || ''}
                  >
                    {modelTypes.map((type) => (
                      <MenuItem key={type.value} value={type.value}>
                        {type.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  name="description"
                  multiline
                  rows={4}
                  defaultValue={selectedModel?.description}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              startIcon={selectedModel ? <EditIcon /> : <AddIcon />}
            >
              {selectedModel ? 'Update' : 'Add'} Model
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      <Dialog
        open={openMetricsDialog}
        onClose={() => setOpenMetricsDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Model Metrics</DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Box sx={{ height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={selectedModel?.metrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="accuracy"
                      stroke="#8884d8"
                      name="Accuracy"
                    />
                    <Line
                      type="monotone"
                      dataKey="precision"
                      stroke="#82ca9d"
                      name="Precision"
                    />
                    <Line
                      type="monotone"
                      dataKey="recall"
                      stroke="#ffc658"
                      name="Recall"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenMetricsDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

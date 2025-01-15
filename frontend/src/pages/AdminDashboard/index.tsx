import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Tab,
  Tabs,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Card,
  CardContent,
  IconButton,
  Button,
  Switch,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Settings as SettingsIcon,
  Flag as FlagIcon,
  History as HistoryIcon,
  Timeline as TimelineIcon,
  Group as GroupIcon,
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
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { format, formatDistanceToNow } from 'date-fns';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const AdminDashboard = () => {
  const [tabValue, setTabValue] = useState(0);
  const [settingsDialogOpen, setSettingsDialogOpen] = useState(false);
  const [selectedSetting, setSelectedSetting] = useState<any>(null);
  const queryClient = useQueryClient();

  // Queries
  const { data: metrics } = useQuery('systemMetrics', () =>
    axios.get('/api/admin/metrics/').then((res) => res.data)
  );

  const { data: auditLogs } = useQuery('auditLogs', () =>
    axios.get('/api/admin/audit-logs/').then((res) => res.data)
  );

  const { data: userActivity } = useQuery('userActivity', () =>
    axios.get('/api/admin/user-activity/').then((res) => res.data)
  );

  const { data: settings } = useQuery('adminSettings', () =>
    axios.get('/api/admin/settings/').then((res) => res.data)
  );

  const { data: featureFlags } = useQuery('featureFlags', () =>
    axios.get('/api/admin/feature-flags/').then((res) => res.data)
  );

  // Mutations
  const updateSettingMutation = useMutation(
    (setting: any) =>
      axios.put(`/api/admin/settings/${setting.id}/`, setting),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('adminSettings');
        setSettingsDialogOpen(false);
      },
    }
  );

  const updateFeatureFlagMutation = useMutation(
    (flag: any) =>
      axios.put(`/api/admin/feature-flags/${flag.id}/`, flag),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('featureFlags');
      },
    }
  );

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleSettingEdit = (setting: any) => {
    setSelectedSetting(setting);
    setSettingsDialogOpen(true);
  };

  const handleSettingSave = () => {
    if (selectedSetting) {
      updateSettingMutation.mutate(selectedSetting);
    }
  };

  const handleFeatureFlagToggle = (flag: any) => {
    updateFeatureFlagMutation.mutate({
      ...flag,
      is_enabled: !flag.is_enabled,
    });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Overview" />
          <Tab label="System Metrics" />
          <Tab label="Audit Logs" />
          <Tab label="User Activity" />
          <Tab label="Settings" />
          <Tab label="Feature Flags" />
        </Tabs>
      </Box>

      {/* Overview Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          {/* Quick Stats */}
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Active Users
                </Typography>
                <Typography variant="h4">
                  {metrics?.active_users || 0}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Error Rate
                </Typography>
                <Typography variant="h4">
                  {metrics?.error_rate?.toFixed(2) || 0}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  CPU Usage
                </Typography>
                <Typography variant="h4">
                  {metrics?.cpu_usage?.toFixed(1) || 0}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Memory Usage
                </Typography>
                <Typography variant="h4">
                  {metrics?.memory_usage?.toFixed(1) || 0}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Charts */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                System Performance
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={metrics?.performance_history || []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={(time) => format(new Date(time), 'HH:mm')}
                  />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="cpu"
                    stroke="#8884d8"
                    name="CPU Usage"
                  />
                  <Line
                    type="monotone"
                    dataKey="memory"
                    stroke="#82ca9d"
                    name="Memory Usage"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Activity Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={userActivity?.distribution || []}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    label
                  >
                    {(userActivity?.distribution || []).map((entry: any, index: number) => (
                      <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>

      {/* System Metrics Tab */}
      <TabPanel value={tabValue} index={1}>
        <Paper sx={{ p: 2 }}>
          <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between' }}>
            <Typography variant="h6">System Metrics History</Typography>
            <IconButton>
              <RefreshIcon />
            </IconButton>
          </Box>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={metrics?.detailed_history || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={(time) => format(new Date(time), 'MM/dd HH:mm')}
              />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="cpu" stroke="#8884d8" name="CPU" />
              <Line
                type="monotone"
                dataKey="memory"
                stroke="#82ca9d"
                name="Memory"
              />
              <Line
                type="monotone"
                dataKey="disk"
                stroke="#ffc658"
                name="Disk"
              />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      </TabPanel>

      {/* Audit Logs Tab */}
      <TabPanel value={tabValue} index={2}>
        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Time</TableCell>
                  <TableCell>User</TableCell>
                  <TableCell>Action</TableCell>
                  <TableCell>Model</TableCell>
                  <TableCell>Details</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {(auditLogs || []).map((log: any) => (
                  <TableRow key={log.id}>
                    <TableCell>
                      {formatDistanceToNow(new Date(log.timestamp), {
                        addSuffix: true,
                      })}
                    </TableCell>
                    <TableCell>{log.user}</TableCell>
                    <TableCell>{log.action}</TableCell>
                    <TableCell>{log.model_name}</TableCell>
                    <TableCell>{log.object_repr}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </TabPanel>

      {/* User Activity Tab */}
      <TabPanel value={tabValue} index={3}>
        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Time</TableCell>
                  <TableCell>User</TableCell>
                  <TableCell>Activity Type</TableCell>
                  <TableCell>Details</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {(userActivity?.logs || []).map((activity: any) => (
                  <TableRow key={activity.id}>
                    <TableCell>
                      {formatDistanceToNow(new Date(activity.timestamp), {
                        addSuffix: true,
                      })}
                    </TableCell>
                    <TableCell>{activity.user}</TableCell>
                    <TableCell>{activity.activity_type}</TableCell>
                    <TableCell>
                      {activity.page_url ||
                        activity.feature_name ||
                        activity.api_endpoint ||
                        activity.error_message}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </TabPanel>

      {/* Settings Tab */}
      <TabPanel value={tabValue} index={4}>
        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Key</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Value</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {(settings || []).map((setting: any) => (
                  <TableRow key={setting.id}>
                    <TableCell>{setting.key}</TableCell>
                    <TableCell>{setting.setting_type}</TableCell>
                    <TableCell>
                      {typeof setting.value === 'object'
                        ? JSON.stringify(setting.value)
                        : setting.value}
                    </TableCell>
                    <TableCell>
                      <IconButton onClick={() => handleSettingEdit(setting)}>
                        <SettingsIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </TabPanel>

      {/* Feature Flags Tab */}
      <TabPanel value={tabValue} index={5}>
        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {(featureFlags || []).map((flag: any) => (
                  <TableRow key={flag.id}>
                    <TableCell>{flag.name}</TableCell>
                    <TableCell>{flag.description}</TableCell>
                    <TableCell>
                      <Switch
                        checked={flag.is_enabled}
                        onChange={() => handleFeatureFlagToggle(flag)}
                      />
                    </TableCell>
                    <TableCell>
                      <IconButton>
                        <SettingsIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </TabPanel>

      {/* Settings Dialog */}
      <Dialog
        open={settingsDialogOpen}
        onClose={() => setSettingsDialogOpen(false)}
      >
        <DialogTitle>Edit Setting</DialogTitle>
        <DialogContent>
          {selectedSetting && (
            <>
              <TextField
                fullWidth
                label="Key"
                value={selectedSetting.key}
                disabled
                margin="normal"
              />
              <TextField
                fullWidth
                label="Value"
                value={
                  typeof selectedSetting.value === 'object'
                    ? JSON.stringify(selectedSetting.value)
                    : selectedSetting.value
                }
                onChange={(e) =>
                  setSelectedSetting({
                    ...selectedSetting,
                    value: e.target.value,
                  })
                }
                margin="normal"
              />
              <TextField
                fullWidth
                label="Description"
                value={selectedSetting.description}
                onChange={(e) =>
                  setSelectedSetting({
                    ...selectedSetting,
                    description: e.target.value,
                  })
                }
                margin="normal"
                multiline
                rows={3}
              />
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSettingsDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSettingSave} variant="contained" color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default AdminDashboard;

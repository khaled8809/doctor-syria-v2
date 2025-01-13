import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Grid
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle,
  Notifications,
  Settings,
  Delete
} from '@mui/icons-material';

interface Alert {
  id: string;
  type: 'critical' | 'warning' | 'info' | 'success';
  title: string;
  message: string;
  timestamp: Date;
  source: string;
  status: 'new' | 'acknowledged' | 'resolved';
  priority: 'high' | 'medium' | 'low';
  assignedTo?: string;
}

interface AlertRule {
  id: string;
  name: string;
  condition: string;
  threshold: number;
  priority: 'high' | 'medium' | 'low';
  notifyRoles: string[];
  isActive: boolean;
}

export const SmartAlertSystem: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [rules, setRules] = useState<AlertRule[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [configDialogOpen, setConfigDialogOpen] = useState(false);
  const [newRule, setNewRule] = useState<Partial<AlertRule>>({});

  useEffect(() => {
    // تحميل التنبيهات والقواعد
    fetchAlerts();
    fetchRules();
  }, []);

  const fetchAlerts = async () => {
    // API call to fetch alerts
  };

  const fetchRules = async () => {
    // API call to fetch rules
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'critical':
        return <Error color="error" />;
      case 'warning':
        return <Warning color="warning" />;
      case 'success':
        return <CheckCircle color="success" />;
      default:
        return <Info color="info" />;
    }
  };

  const handleAlertAction = async (alertId: string, action: string) => {
    // تحديث حالة التنبيه
  };

  const handleRuleChange = async (ruleId: string, changes: Partial<AlertRule>) => {
    // تحديث قواعد التنبيهات
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">نظام التنبيهات الذكي</Typography>
        <Button
          variant="contained"
          startIcon={<Settings />}
          onClick={() => setConfigDialogOpen(true)}
        >
          إعدادات التنبيهات
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Active Alerts */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              التنبيهات النشطة
            </Typography>
            <List>
              {alerts.map((alert) => (
                <ListItem
                  key={alert.id}
                  sx={{
                    mb: 1,
                    border: 1,
                    borderColor: 'divider',
                    borderRadius: 1,
                    '&:hover': {
                      backgroundColor: 'action.hover',
                    },
                  }}
                >
                  <ListItemIcon>
                    {getAlertIcon(alert.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {alert.title}
                        <Chip
                          size="small"
                          label={alert.priority}
                          color={alert.priority === 'high' ? 'error' : 'default'}
                        />
                      </Box>
                    }
                    secondary={
                      <>
                        {alert.message}
                        <br />
                        <Typography variant="caption" color="text.secondary">
                          {new Date(alert.timestamp).toLocaleString('ar-SA')}
                        </Typography>
                      </>
                    }
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      onClick={() => handleAlertAction(alert.id, 'acknowledge')}
                    >
                      <CheckCircle />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Alert Rules */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              قواعد التنبيهات
            </Typography>
            <List>
              {rules.map((rule) => (
                <ListItem
                  key={rule.id}
                  sx={{
                    mb: 1,
                    border: 1,
                    borderColor: 'divider',
                    borderRadius: 1,
                  }}
                >
                  <ListItemText
                    primary={rule.name}
                    secondary={`الأولوية: ${rule.priority}`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      onClick={() => handleRuleChange(rule.id, { isActive: !rule.isActive })}
                    >
                      {rule.isActive ? <CheckCircle color="success" /> : <Error color="error" />}
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Configuration Dialog */}
      <Dialog
        open={configDialogOpen}
        onClose={() => setConfigDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>إعدادات التنبيهات</DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="اسم القاعدة"
                value={newRule.name}
                onChange={(e) => setNewRule({ ...newRule, name: e.target.value })}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                select
                label="الأولوية"
                value={newRule.priority}
                onChange={(e) => setNewRule({ ...newRule, priority: e.target.value as 'high' | 'medium' | 'low' })}
                margin="normal"
              >
                <MenuItem value="high">عالية</MenuItem>
                <MenuItem value="medium">متوسطة</MenuItem>
                <MenuItem value="low">منخفضة</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="شرط التنبيه"
                value={newRule.condition}
                onChange={(e) => setNewRule({ ...newRule, condition: e.target.value })}
                margin="normal"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfigDialogOpen(false)}>إلغاء</Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              // حفظ القاعدة الجديدة
              setConfigDialogOpen(false);
            }}
          >
            حفظ
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SmartAlertSystem;

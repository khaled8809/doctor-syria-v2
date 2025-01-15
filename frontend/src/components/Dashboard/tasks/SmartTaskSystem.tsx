import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  IconButton,
  Button,
  Chip,
  Avatar,
  LinearProgress,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  ListItemSecondaryAction
} from '@mui/material';
import {
  Assignment,
  Add,
  Person,
  Schedule,
  TrendingUp,
  Speed,
  AutoGraph,
  PlayArrow,
  Pause,
  Done,
  Timeline
} from '@mui/icons-material';

interface Task {
  id: string;
  title: string;
  description: string;
  assignedTo: string;
  priority: 'high' | 'medium' | 'low';
  status: 'pending' | 'in_progress' | 'completed';
  deadline: Date;
  progress: number;
  category: string;
  estimatedTime: number;
  actualTime: number;
  dependencies: string[];
}

interface Employee {
  id: string;
  name: string;
  role: string;
  department: string;
  efficiency: number;
  currentLoad: number;
  skills: string[];
  avatar: string;
}

export const SmartTaskSystem: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [newTaskDialog, setNewTaskDialog] = useState(false);
  const [taskMetrics, setTaskMetrics] = useState({
    efficiency: 0,
    completion: 0,
    overdue: 0
  });

  useEffect(() => {
    // تحميل البيانات الأولية
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    // API calls to fetch tasks and employees
  };

  const handleTaskAssignment = (task: Task) => {
    // الخوارزمية الذكية لتوزيع المهام
    const recommendedEmployee = employees.reduce((best, current) => {
      const score = calculateAssignmentScore(current, task);
      return score > calculateAssignmentScore(best, task) ? current : best;
    }, employees[0]);

    return recommendedEmployee;
  };

  const calculateAssignmentScore = (employee: Employee, task: Task) => {
    // حساب درجة ملاءمة الموظف للمهمة
    const skillMatch = employee.skills.filter(skill =>
      task.category.includes(skill)).length;
    const workloadFactor = 1 - (employee.currentLoad / 100);
    const efficiencyFactor = employee.efficiency / 100;

    return (skillMatch * 0.4) + (workloadFactor * 0.3) + (efficiencyFactor * 0.3);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">نظام المهام الذكي</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setNewTaskDialog(true)}
        >
          مهمة جديدة
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Performance Metrics */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                مؤشرات الأداء
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">كفاءة الفريق</Typography>
                  <Typography variant="body2">{taskMetrics.efficiency}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={taskMetrics.efficiency}
                  color="primary"
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">نسبة الإنجاز</Typography>
                  <Typography variant="body2">{taskMetrics.completion}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={taskMetrics.completion}
                  color="success"
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
              <Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">المهام المتأخرة</Typography>
                  <Typography variant="body2">{taskMetrics.overdue}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={taskMetrics.overdue}
                  color="error"
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Team Workload */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              توزيع العمل
            </Typography>
            <List>
              {employees.map((employee) => (
                <ListItem key={employee.id}>
                  <ListItemAvatar>
                    <Avatar src={employee.avatar} />
                  </ListItemAvatar>
                  <ListItemText
                    primary={employee.name}
                    secondary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Chip
                          label={employee.role}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                        <Typography variant="body2" color="text.secondary">
                          كفاءة: {employee.efficiency}%
                        </Typography>
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <Box sx={{ width: 100 }}>
                      <Typography variant="caption" align="center">
                        العبء الحالي
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={employee.currentLoad}
                        color={employee.currentLoad > 80 ? 'error' : 'primary'}
                      />
                    </Box>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Active Tasks */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              المهام النشطة
            </Typography>
            <Grid container spacing={2}>
              {tasks.map((task) => (
                <Grid item xs={12} md={4} key={task.id}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                        <Typography variant="subtitle1">{task.title}</Typography>
                        <Chip
                          label={task.priority}
                          color={
                            task.priority === 'high' ? 'error' :
                            task.priority === 'medium' ? 'warning' : 'info'
                          }
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        {task.description}
                      </Typography>
                      <Box sx={{ mt: 2 }}>
                        <LinearProgress
                          variant="determinate"
                          value={task.progress}
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                          <Typography variant="caption">
                            التقدم: {task.progress}%
                          </Typography>
                          <Typography variant="caption">
                            المتبقي: {task.estimatedTime - task.actualTime} ساعات
                          </Typography>
                        </Box>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>

      {/* New Task Dialog */}
      <Dialog
        open={newTaskDialog}
        onClose={() => setNewTaskDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>إضافة مهمة جديدة</DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="عنوان المهمة"
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="وصف المهمة"
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                select
                label="الأولوية"
                margin="normal"
              >
                <MenuItem value="high">عالية</MenuItem>
                <MenuItem value="medium">متوسطة</MenuItem>
                <MenuItem value="low">منخفضة</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="الوقت المتوقع (ساعات)"
                margin="normal"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewTaskDialog(false)}>إلغاء</Button>
          <Button variant="contained" color="primary">
            إضافة المهمة
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SmartTaskSystem;

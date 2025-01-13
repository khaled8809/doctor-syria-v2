import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from '../../../hooks/useAuth';
import { useSocket } from '../../../hooks/useSocket';
import { useNurseStats } from '../../../hooks/useNurseStats';
import { useDoctorStats } from '../../../hooks/useDoctorStats';
import {
  User,
  Notification,
  Patient,
  Resource,
  Task,
  Medication,
  Analytics,
  NurseStats,
  DoctorStats,
  Appointment
} from '../../../types/common';

interface SharedState {
  currentUser: User | null;
  notifications: Notification[];
  activePatients: Patient[];
  resources: Resource[];
  tasks: Task[];
  appointments: Appointment[];
  medications: Medication[];
  analytics: Analytics;
  lastUpdate: Date;
}

interface DashboardContextType {
  state: SharedState;
  updateState: (updates: Partial<SharedState>) => void;
  refreshData: () => Promise<void>;
  sendNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  updateTask: (taskId: string, updates: Partial<Task>) => Promise<void>;
  updateResource: (resourceId: string, updates: Partial<Resource>) => Promise<void>;
}

const DashboardContext = createContext<DashboardContextType | null>(null);

export const useDashboard = () => {
  const context = useContext(DashboardContext);
  if (!context) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
};

export const DashboardProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const socket = useSocket();
  const nurseStats = useNurseStats();
  const doctorStats = useDoctorStats();

  const [state, setState] = useState<SharedState>({
    currentUser: user,
    notifications: [],
    activePatients: [],
    resources: [],
    tasks: [],
    appointments: [],
    medications: [],
    analytics: {
      patientMetrics: {
        total: 0,
        admitted: 0,
        discharged: 0,
        critical: 0,
      },
      resourceMetrics: {
        utilization: 0,
        shortage: [],
        excess: [],
      },
      performanceMetrics: {
        taskCompletion: 0,
        responseTime: 0,
        patientSatisfaction: 0,
      },
      nurseMetrics: {
        currentShift: '',
        totalPatients: 0,
        criticalCases: 0,
        pendingTasks: 0,
        completedTasks: 0,
      },
      doctorStats: {
        todayAppointments: 0,
        emergencyCases: 0,
        activePatients: 0,
        newLabResults: 0,
      },
    },
    lastUpdate: new Date()
  });

  const updateState = (updates: Partial<SharedState>) => {
    setState(prev => ({
      ...prev,
      ...updates,
      lastUpdate: new Date()
    }));
  };

  const refreshData = async () => {
    try {
      if (nurseStats) {
        updateState({
          tasks: nurseStats.tasks,
          medications: nurseStats.medications,
          activePatients: nurseStats.patients
        });
      }

      if (doctorStats) {
        updateState({
          appointments: doctorStats.appointments,
          analytics: {
            ...state.analytics,
            doctorStats: doctorStats.stats
          }
        });
      }

      const [resourcesRes, analyticsRes] = await Promise.all([
        fetch('/api/resources/status'),
        fetch('/api/analytics/dashboard')
      ]);

      const [resources, analytics] = await Promise.all([
        resourcesRes.json(),
        analyticsRes.json()
      ]);

      updateState({
        resources,
        analytics: {
          ...state.analytics,
          ...analytics
        }
      });

    } catch (error) {
      console.error('Error refreshing dashboard data:', error);
    }
  };

  const sendNotification = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    socket?.emit('notification', notification);
    updateState({
      notifications: [...state.notifications, { ...notification, id: Math.random().toString(), timestamp: new Date(), read: false }]
    });
  };

  const updateTask = async (taskId: string, updates: Partial<Task>) => {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updates)
      });

      if (!response.ok) throw new Error('فشل تحديث المهمة');

      const updatedTask = await response.json();
      updateState({
        tasks: state.tasks.map(task => 
          task.id === taskId ? { ...task, ...updatedTask } : task
        )
      });

      sendNotification({
        type: 'info',
        message: 'تم تحديث المهمة بنجاح'
      });

    } catch (error) {
      console.error('Error updating task:', error);
      sendNotification({
        type: 'error',
        message: 'فشل تحديث المهمة'
      });
    }
  };

  const updateResource = async (resourceId: string, updates: Partial<Resource>) => {
    try {
      const response = await fetch(`/api/resources/${resourceId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updates)
      });

      if (!response.ok) throw new Error('فشل تحديث المورد');

      const updatedResource = await response.json();
      updateState({
        resources: state.resources.map(resource => 
          resource.id === resourceId ? { ...resource, ...updatedResource } : resource
        )
      });

      sendNotification({
        type: 'info',
        message: 'تم تحديث المورد بنجاح'
      });

    } catch (error) {
      console.error('Error updating resource:', error);
      sendNotification({
        type: 'error',
        message: 'فشل تحديث المورد'
      });
    }
  };

  useEffect(() => {
    if (socket) {
      socket.on('state_update', (updates: Partial<SharedState>) => {
        const processedUpdates = {
          ...updates,
          tasks: updates.tasks?.map(task => ({
            ...task,
            assignedTo: task.assignedTo || '',
            dueDate: new Date(task.dueDate || new Date()),
            status: task.status || 'pending',
            priority: task.priority || 'medium'
          })) as Task[],
          medications: updates.medications?.map(med => ({
            ...med,
            name: med.name || '',
            patientId: med.patientId || '',
            status: med.status || 'pending',
            nextDose: new Date(med.nextDose || new Date())
          })) as Medication[],
          activePatients: updates.activePatients?.map(patient => ({
            ...patient,
            condition: patient.condition || 'stable',
            lastUpdate: new Date(patient.lastUpdate || new Date())
          })) as Patient[]
        };
        updateState(processedUpdates);
      });

      socket.on('notification', (notification: Notification) => {
        updateState({
          notifications: [...state.notifications, notification]
        });
      });

      return () => {
        socket.off('state_update');
        socket.off('notification');
      };
    }
  }, [socket, state.notifications]);

  useEffect(() => {
    if (doctorStats) {
      updateState({
        analytics: {
          ...state.analytics,
          doctorStats: doctorStats.stats
        }
      });
    }
  }, [doctorStats]);

  useEffect(() => {
    if (nurseStats) {
      updateState({
        analytics: {
          ...state.analytics,
          nurseMetrics: {
            currentShift: nurseStats.stats.currentShift,
            totalPatients: nurseStats.stats.totalPatients,
            criticalCases: nurseStats.stats.criticalCases,
            pendingTasks: nurseStats.stats.pendingTasks,
            completedTasks: nurseStats.stats.completedTasks
          }
        }
      });
    }
  }, [nurseStats]);

  useEffect(() => {
    if (user) {
      updateState({
        currentUser: user
      });
    }
  }, [user]);

  useEffect(() => {
    updateState({
      lastUpdate: new Date()
    });
  }, [state.analytics, state.activePatients, state.tasks, state.medications]);

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 60000); 

    return () => clearInterval(interval);
  }, []);

  return (
    <DashboardContext.Provider
      value={{
        state,
        updateState,
        refreshData,
        sendNotification,
        updateTask,
        updateResource
      }}
    >
      {children}
    </DashboardContext.Provider>
  );
};

export default DashboardProvider;

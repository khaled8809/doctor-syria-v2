// تعريفات الأنواع المشتركة
export interface User {
  id: string;
  name: string;
  role: string;
  department?: string;
  permissions: string[];
  avatar?: string;
}

export interface Notification {
  id: string;
  type: 'info' | 'warning' | 'error' | 'success';
  message: string;
  timestamp: Date;
  read: boolean;
}

export interface Patient {
  id: string;
  name: string;
  roomNumber?: string;
  condition: string;
  vitals?: {
    temperature: number;
    bloodPressure: string;
    heartRate: number;
    oxygenSaturation: number;
  };
  lastUpdate: Date;
}

export interface PatientVital extends Patient {
  status: 'normal' | 'warning' | 'critical';
}

export interface Resource {
  id: string;
  name: string;
  category: string;
  quantity: number;
  unit: string;
  status: 'available' | 'low' | 'critical';
}

export interface Task {
  id: string;
  title: string;
  description: string;
  assignedTo: string;
  patientName?: string;
  roomNumber?: string;
  priority: 'high' | 'medium' | 'low';
  status: 'pending' | 'in_progress' | 'completed';
  dueDate: Date;
  time: string;
  notes?: string;
}

export interface Medication {
  id: string;
  name: string;
  dosage: string;
  frequency: string;
  patientId: string;
  patientName: string;
  roomNumber?: string;
  status: 'pending' | 'given' | 'missed' | 'delayed';
  nextDose: Date;
  instructions?: string;
  notes?: string;
  medicationName: string;
}

export interface NurseStats {
  currentShift: string;
  totalPatients: number;
  criticalCases: number;
  pendingTasks: number;
  completedTasks: number;
}

export interface DoctorStats {
  todayAppointments: number;
  emergencyCases: number;
  activePatients: number;
  newLabResults: number;
}

export interface Appointment {
  id: string;
  patientId: string;
  patientName: string;
  doctorId: string;
  doctorName: string;
  date: Date;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  type: string;
  notes?: string;
  duration?: number;
  room?: string;
  priority?: 'normal' | 'urgent';
}

export interface Analytics {
  patientMetrics: {
    total: number;
    admitted: number;
    discharged: number;
    critical: number;
  };
  resourceMetrics: {
    utilization: number;
    shortage: string[];
    excess: string[];
  };
  performanceMetrics: {
    taskCompletion: number;
    responseTime: number;
    patientSatisfaction: number;
  };
  predictions: {
    id: string;
    type: string;
    prediction: string;
    confidence: number;
    actions: string[];
  }[];
  departmentPerformance: {
    department: string;
    metrics: {
      efficiency: number;
      satisfaction: number;
      utilization: number;
    };
  }[];
  resourceUtilization: {
    resource: string;
    usage: number;
    trend: 'increasing' | 'stable' | 'decreasing';
  }[];
  financialMetrics: {
    revenue: number;
    expenses: number;
    profit: number;
    trend: 'up' | 'down' | 'stable';
  };
  nurseMetrics: NurseStats;
  doctorStats: DoctorStats;
}

export interface AIModel {
  id: string;
  name: string;
  version: string;
  type: string;
  status: 'active' | 'inactive' | 'training';
  accuracy: number;
  lastUpdated: Date;
  description: string;
  metrics: {
    precision: number;
    recall: number;
    f1Score: number;
  };
}

export interface DiagnosisResult {
  id: string;
  patientId: string;
  symptoms: string[];
  diagnosis: string;
  confidence: number;
  recommendations: string[];
  timestamp: Date;
}

export interface ResourcePrediction {
  resourceId: string;
  resourceName: string;
  predictedDemand: number;
  confidence: number;
  timeframe: string;
}

export interface ResourceNeed {
  resourceId: string;
  resourceName: string;
  currentStock: number;
  minimumRequired: number;
  recommendedAction: string;
}

export interface Reminder {
  id: string;
  medicationName: string;
  dosage: string;
  time: Date;
  active: boolean;
  taken: boolean;
}

export interface ScheduleEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  resourceId?: string;
  color?: string;
  type: 'appointment' | 'surgery' | 'meeting' | 'break';
  status: 'scheduled' | 'in-progress' | 'completed' | 'cancelled';
}

// تعريفات الأنواع المشتركة
export interface User {
  id: string;
  name: string;
  role: string;
  department?: string;
  permissions: string[];
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
  nurseMetrics: NurseStats;
  doctorStats: DoctorStats;
}

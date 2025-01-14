export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  avatar?: string;
}

export interface Patient {
  id: string;
  name: string;
  dateOfBirth: string;
  gender: string;
  contactNumber: string;
  address: string;
  medicalHistory?: string[];
  currentMedications?: string[];
  allergies?: string[];
}

export interface PatientVital {
  id: string;
  patientId: string;
  temperature: number;
  bloodPressure: string;
  heartRate: number;
  respiratoryRate: number;
  oxygenSaturation: number;
  timestamp: string;
  status: 'normal' | 'warning' | 'critical';
}

export interface Task {
  id: string;
  title: string;
  description: string;
  assignedTo: string;
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'in-progress' | 'completed';
  dueDate: string;
  time: string;
}

export interface Medication {
  id: string;
  medicationName: string;
  dosage: string;
  frequency: string;
  startDate: string;
  endDate: string;
  instructions: string;
  prescribedBy: string;
}

export interface Resource {
  id: string;
  name: string;
  type: string;
  status: 'available' | 'in-use' | 'maintenance' | 'unavailable';
  lastMaintenance?: string;
  nextMaintenance?: string;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'warning' | 'error' | 'success';
  timestamp: string;
  read: boolean;
}

export interface Analytics {
  patientCount: number;
  appointmentCount: number;
  emergencyCount: number;
  resourceUtilization: {
    beds: number;
    equipment: number;
    staff: number;
  };
  departmentPerformance: {
    emergency: number;
    surgery: number;
    pediatrics: number;
    cardiology: number;
  };
  financialMetrics: {
    revenue: number;
    expenses: number;
    profit: number;
  };
  predictions?: {
    patientFlow: number;
    resourceNeeds: number;
    staffingRequirements: number;
  };
}

export interface DiagnosisResult {
  id: string;
  patientId: string;
  symptoms: string[];
  diagnosis: string;
  confidence: number;
  recommendations: string[];
  timestamp: string;
}

export interface ResourcePrediction {
  resourceType: string;
  predictedDemand: number;
  confidence: number;
  timeframe: string;
}

export interface ResourceNeed {
  resourceType: string;
  currentStock: number;
  recommendedStock: number;
  urgency: 'low' | 'medium' | 'high';
}

export interface Reminder {
  id: string;
  medicationName: string;
  dosage: string;
  time: Date;
  active: boolean;
  taken: boolean;
}

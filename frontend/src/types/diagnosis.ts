export interface DiagnosisResult {
  id: string;
  patientId: string;
  diagnosis: string;
  riskLevel: 'low' | 'medium' | 'high';
  timestamp: string;
  symptoms: string[];
  recommendations: string[];
  confidence: number;
  doctorId?: string;
}

export interface HealthRisk {
  level: 'low' | 'medium' | 'high';
  description: string;
  recommendations: string[];
}

export interface HealthMetric {
  name: string;
  value: number;
  unit: string;
  normalRange: {
    min: number;
    max: number;
  };
}

export interface SymptomInput {
  symptom_id: number;
  symptom: string;
  severity: number;
  notes?: string;
}

export interface ResourcePrediction {
  resourceType: string;
  probability: number;
  estimatedQuantity: number;
  timeframe: string;
}

export interface ResourceNeed {
  resourceType: string;
  quantity: number;
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'fulfilled' | 'cancelled';
}

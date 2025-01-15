export interface DiagnosisResult {
  id: string;
  patientId: string;
  symptoms: string[];
  diagnosis: string;
  confidence: number;
  recommendations: string[];
  riskLevel: 'low' | 'medium' | 'high';
  timestamp: Date;
  doctorNotes?: string;
  followUpDate?: Date;
}

export interface Symptom {
  id: string;
  name: string;
  description?: string;
  severity: 'mild' | 'moderate' | 'severe';
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

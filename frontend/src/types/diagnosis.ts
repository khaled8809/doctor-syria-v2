export interface DiagnosisResult {
  id: string | number;
  patientId: number;
  diagnosis: string;
  confidence: number;
  recommendations: string[];
  riskLevel: 'low' | 'medium' | 'high';
  timestamp: string;
  details?: {
    icd_code?: string;
    matching_symptoms?: {
      name: string;
      importance: number;
    }[];
    missing_symptoms?: {
      name: string;
      importance: number;
    }[];
    confidence_explanation?: string;
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

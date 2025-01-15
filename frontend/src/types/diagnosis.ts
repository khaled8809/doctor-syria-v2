export interface DiagnosisResult {
  id: string;
  diagnosis: {
    name: string;
    icd_code: string;
    risk_level: number;
  };
  confidence: number;
  reasoning: {
    matching_symptoms: {
      name: string;
      importance: number;
    }[];
    missing_symptoms: {
      name: string;
      importance: number;
    }[];
    confidence_explanation: string;
  };
  recommendations: string[];
  riskLevel: 'low' | 'medium' | 'high';
}

export interface Symptom {
  symptom_id: number;
  name: string;
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

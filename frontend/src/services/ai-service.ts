import { useState, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

interface Symptom {
  id: number;
  name: string;
  description: string;
  severity_level: number;
  keywords: string[];
}

interface DiagnosisInput {
  patientId: number;
  symptoms: Array<{
    symptom_id: number;
    severity: number;
    notes?: string;
  }>;
  notes?: string;
}

interface DiagnosisResult {
  disease: {
    name: string;
    icd_code: string;
    risk_level: number;
  };
  confidence: number;
  reasoning: {
    matching_symptoms: Array<{
      name: string;
      importance: number;
    }>;
    missing_symptoms: Array<{
      name: string;
      importance: number;
    }>;
    confidence_explanation: string;
  };
  recommendations: string;
}

interface PredictionInput {
  startDate: Date;
  endDate: Date;
  parameters?: Record<string, any>;
}

interface AIServiceError {
  message: string;
  code: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

export const useAIService = () => {
  const { getAuthHeaders } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<AIServiceError | null>(null);

  const handleRequest = useCallback(async <T>(
    request: Promise<{ data: T }>
  ): Promise<T> => {
    try {
      setLoading(true);
      setError(null);
      const response = await request;
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'حدث خطأ غير متوقع';
      setError({
        message: errorMessage,
        code: 'REQUEST_ERROR',
      });
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getSymptoms = useCallback(async (): Promise<Symptom[]> => {
    return handleRequest(
      axios.get(`${API_BASE_URL}/api/symptoms/`, {
        headers: getAuthHeaders(),
      })
    );
  }, [getAuthHeaders, handleRequest]);

  const startDiagnosis = useCallback(async (
    input: DiagnosisInput
  ): Promise<DiagnosisResult[]> => {
    return handleRequest(
      axios.post(`${API_BASE_URL}/api/diagnosis/start/`, input, {
        headers: getAuthHeaders(),
      })
    );
  }, [getAuthHeaders, handleRequest]);

  const getDiagnosisResults = useCallback(async (
    sessionId: number
  ): Promise<DiagnosisResult[]> => {
    return handleRequest(
      axios.get(`${API_BASE_URL}/api/diagnosis/${sessionId}/results/`, {
        headers: getAuthHeaders(),
      })
    );
  }, [getAuthHeaders, handleRequest]);

  const predictPatientRisks = useCallback(async (
    patientId: number
  ): Promise<any> => {
    return handleRequest(
      axios.post(`${API_BASE_URL}/api/predictions/patient-risks/`, {
        patient_id: patientId,
      }, {
        headers: getAuthHeaders(),
      })
    );
  }, [getAuthHeaders, handleRequest]);

  const predictAppointmentLoad = useCallback(async (
    input: PredictionInput
  ): Promise<any> => {
    return handleRequest(
      axios.post(`${API_BASE_URL}/api/predictions/appointment-load/`, input, {
        headers: getAuthHeaders(),
      })
    );
  }, [getAuthHeaders, handleRequest]);

  const predictResourceNeeds = useCallback(async (
    timeframe: string
  ): Promise<any> => {
    return handleRequest(
      axios.post(`${API_BASE_URL}/api/predictions/resource-needs/`, {
        timeframe,
      }, {
        headers: getAuthHeaders(),
      })
    );
  }, [getAuthHeaders, handleRequest]);

  return {
    loading,
    error,
    getSymptoms,
    startDiagnosis,
    getDiagnosisResults,
    predictPatientRisks,
    predictAppointmentLoad,
    predictResourceNeeds,
  };
};

export default useAIService;

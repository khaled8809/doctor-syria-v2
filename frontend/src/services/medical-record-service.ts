import { useState, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

export interface MedicalRecord {
  id: number;
  patientId: number;
  date: string;
  diagnosisResults: any[];
  symptoms: any[];
  doctorId: number;
  notes?: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

export function useMedicalRecordService() {
  const { getAuthHeaders } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const saveMedicalRecord = useCallback(async (record: Partial<MedicalRecord>) => {
    return handleRequest(
      axios.post<MedicalRecord>(
        `${API_BASE_URL}/api/medical-records/`,
        record,
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const getMedicalRecords = useCallback(async (patientId: number) => {
    return handleRequest(
      axios.get<MedicalRecord[]>(
        `${API_BASE_URL}/api/medical-records/patient/${patientId}/`,
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const updateMedicalRecord = useCallback(async (
    recordId: number,
    updates: Partial<MedicalRecord>
  ) => {
    return handleRequest(
      axios.patch<MedicalRecord>(
        `${API_BASE_URL}/api/medical-records/${recordId}/`,
        updates,
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const addFollowUp = useCallback(async (
    recordId: number,
    followUpData: {
      date: string;
      notes: string;
      doctorId: number;
    }
  ) => {
    return handleRequest(
      axios.post(
        `${API_BASE_URL}/api/medical-records/${recordId}/follow-up/`,
        followUpData,
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const generateReport = useCallback(async (recordId: number) => {
    return handleRequest(
      axios.get(
        `${API_BASE_URL}/api/medical-records/${recordId}/report/`,
        {
          headers: getAuthHeaders(),
          responseType: 'blob',
        }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  return {
    loading,
    error,
    saveMedicalRecord,
    getMedicalRecords,
    updateMedicalRecord,
    addFollowUp,
    generateReport,
  };
}

import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';

interface Patient {
  id: string;
  name: string;
  age: number;
  gender: string;
  medicalHistory: string[];
  currentMedications: string[];
  allergies: string[];
  bloodType: string;
  lastVisit: Date;
}

interface PatientContextType {
  currentPatient: Patient | null;
  setCurrentPatient: (patient: Patient | null) => void;
  loading: boolean;
  error: string | null;
  fetchPatient: (id: string) => Promise<void>;
  updatePatient: (data: Partial<Patient>) => Promise<void>;
}

const PatientContext = createContext<PatientContextType | undefined>(undefined);

export const PatientProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentPatient, setCurrentPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPatient = async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`/api/patients/${id}`);
      setCurrentPatient(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch patient data');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updatePatient = async (data: Partial<Patient>) => {
    if (!currentPatient) throw new Error('No patient selected');

    try {
      setLoading(true);
      setError(null);
      const response = await axios.put(`/api/patients/${currentPatient.id}`, data);
      setCurrentPatient(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update patient data');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return (
    <PatientContext.Provider
      value={{
        currentPatient,
        setCurrentPatient,
        loading,
        error,
        fetchPatient,
        updatePatient,
      }}
    >
      {children}
    </PatientContext.Provider>
  );
};

export const usePatientContext = () => {
  const context = useContext(PatientContext);
  if (context === undefined) {
    throw new Error('usePatientContext must be used within a PatientProvider');
  }
  return context;
};

export default PatientProvider;

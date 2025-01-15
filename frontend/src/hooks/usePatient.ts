import { useQuery } from '@tanstack/react-query';
import { Patient } from '../types/patient';
import axios from 'axios';

const fetchPatient = async (id: string): Promise<Patient> => {
  const { data } = await axios.get(`/api/patients/${id}`);
  return data;
};

export const usePatient = (id: string) => {
  return useQuery<Patient, Error>(['patient', id], () => fetchPatient(id), {
    enabled: !!id,
  });
};

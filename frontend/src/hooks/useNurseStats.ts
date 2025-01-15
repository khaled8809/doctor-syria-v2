import { useState, useEffect } from 'react';
import axios from 'axios';
import { Task, Patient, Medication, NurseStats } from '../types/common';

export const useNurseStats = () => {
  const [data, setData] = useState<{
    stats: NurseStats;
    tasks: Task[];
    patients: Patient[];
    medications: Medication[];
    loading: boolean;
    error: string | null;
  }>({
    stats: {
      currentShift: '',
      totalPatients: 0,
      criticalCases: 0,
      pendingTasks: 0,
      completedTasks: 0
    },
    tasks: [],
    patients: [],
    medications: [],
    loading: true,
    error: null
  });

  const fetchData = async () => {
    try {
      const [statsRes, tasksRes, patientsRes, medsRes] = await Promise.all([
        axios.get('/api/nurse/stats'),
        axios.get('/api/nurse/tasks'),
        axios.get('/api/nurse/patients'),
        axios.get('/api/nurse/medications')
      ]);

      setData({
        stats: statsRes.data,
        tasks: tasksRes.data.map((task: any) => ({
          ...task,
          dueDate: new Date(task.dueDate)
        })) as Task[],
        patients: patientsRes.data.map((patient: any) => ({
          ...patient,
          lastUpdate: new Date(patient.lastUpdate)
        })) as Patient[],
        medications: medsRes.data.map((med: any) => ({
          ...med,
          nextDose: new Date(med.nextDose)
        })) as Medication[],
        loading: false,
        error: null
      });
    } catch (error) {
      setData(prev => ({
        ...prev,
        loading: false,
        error: 'فشل في تحميل البيانات'
      }));
    }
  };

  const updateTask = async (taskId: string, status: 'pending' | 'in_progress' | 'completed', notes?: string) => {
    try {
      await axios.patch(`/api/nurse/tasks/${taskId}`, { status, notes });
      setData(prev => ({
        ...prev,
        tasks: prev.tasks.map(task =>
          task.id === taskId
            ? { ...task, status, notes: notes || task.notes } as Task
            : task
        )
      }));
    } catch (err) {
      setData(prev => ({
        ...prev,
        error: 'حدث خطأ في تحديث المهمة'
      }));
    }
  };

  const updateMedication = async (medId: string, status: 'pending' | 'given' | 'missed' | 'delayed', notes?: string) => {
    try {
      await axios.patch(`/api/nurse/medications/${medId}`, { status, notes });
      setData(prev => ({
        ...prev,
        medications: prev.medications.map(med =>
          med.id === medId
            ? { ...med, status, notes: notes || med.notes } as Medication
            : med
        )
      }));
    } catch (err) {
      setData(prev => ({
        ...prev,
        error: 'حدث خطأ في تحديث حالة الدواء'
      }));
    }
  };

  const updateVitals = async (patientId: string, vitals: Patient['vitals']) => {
    try {
      await axios.post(`/api/nurse/patients/${patientId}/vitals`, vitals);
      setData(prev => ({
        ...prev,
        patients: prev.patients.map(patient =>
          patient.id === patientId
            ? { ...patient, vitals, lastUpdate: new Date() } as Patient
            : patient
        )
      }));
    } catch (err) {
      setData(prev => ({
        ...prev,
        error: 'حدث خطأ في تحديث العلامات الحيوية'
      }));
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  return {
    ...data,
    updateTask,
    updateMedication,
    updateVitals
  };
};

export default useNurseStats;

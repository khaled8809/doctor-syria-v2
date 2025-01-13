import { useState, useEffect } from 'react';
import axios from 'axios';

interface DoctorStats {
  todayAppointments: number;
  emergencyCases: number;
  activePatients: number;
  newLabResults: number;
}

interface Patient {
  id: string;
  name: string;
  age: number;
  lastVisit: string;
  condition: string;
}

interface LabResult {
  id: string;
  patientName: string;
  testType: string;
  date: string;
  status: 'pending' | 'reviewed';
  result: string;
}

export const useDoctorStats = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<DoctorStats>({
    todayAppointments: 0,
    emergencyCases: 0,
    activePatients: 0,
    newLabResults: 0
  });
  const [appointments, setAppointments] = useState([]);
  const [patients, setPatients] = useState<Patient[]>([]);
  const [labResults, setLabResults] = useState<LabResult[]>([]);

  useEffect(() => {
    const fetchDoctorData = async () => {
      try {
        setLoading(true);
        
        // يمكن تجميع كل هذه الطلبات في طلب واحد في الباك اند
        const [statsRes, appointmentsRes, patientsRes, labRes] = await Promise.all([
          axios.get('/api/doctor/stats'),
          axios.get('/api/doctor/appointments'),
          axios.get('/api/doctor/patients'),
          axios.get('/api/doctor/lab-results')
        ]);

        setStats(statsRes.data);
        setAppointments(appointmentsRes.data);
        setPatients(patientsRes.data);
        setLabResults(labRes.data);
        
      } catch (err) {
        setError(err instanceof Error ? err.message : 'حدث خطأ في تحميل البيانات');
      } finally {
        setLoading(false);
      }
    };

    fetchDoctorData();
  }, []);

  const refreshData = async () => {
    // إعادة تحميل البيانات
    try {
      setLoading(true);
      const statsRes = await axios.get('/api/doctor/stats');
      setStats(statsRes.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'حدث خطأ في تحديث البيانات');
    } finally {
      setLoading(false);
    }
  };

  return {
    stats,
    appointments,
    patients,
    labResults,
    loading,
    error,
    refreshData
  };
};

export default useDoctorStats;

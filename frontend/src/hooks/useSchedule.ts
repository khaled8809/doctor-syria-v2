import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './useAuth';
import { useNotifications } from './useNotifications';

interface Appointment {
  id: string;
  patientName: string;
  date: Date;
  time: string;
  type: string;
  status: 'scheduled' | 'completed' | 'cancelled';
}

export const useSchedule = () => {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();
  const { addNotification } = useNotifications();

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/appointments');
      setAppointments(response.data);
      setError(null);
    } catch (err) {
      setError('حدث خطأ في تحميل المواعيد');
      addNotification({
        type: 'error',
        message: 'فشل في تحميل المواعيد',
      });
    } finally {
      setLoading(false);
    }
  };

  const addAppointment = async (appointmentData: Omit<Appointment, 'id'>) => {
    try {
      const response = await axios.post('/api/appointments', appointmentData);
      setAppointments([...appointments, response.data]);
      addNotification({
        type: 'success',
        message: 'تم إضافة الموعد بنجاح',
      });
    } catch (err) {
      addNotification({
        type: 'error',
        message: 'فشل في إضافة الموعد',
      });
      throw err;
    }
  };

  const updateAppointment = async (id: string, appointmentData: Partial<Appointment>) => {
    try {
      const response = await axios.put(`/api/appointments/${id}`, appointmentData);
      setAppointments(
        appointments.map((appointment) =>
          appointment.id === id ? { ...appointment, ...response.data } : appointment
        )
      );
      addNotification({
        type: 'success',
        message: 'تم تحديث الموعد بنجاح',
      });
    } catch (err) {
      addNotification({
        type: 'error',
        message: 'فشل في تحديث الموعد',
      });
      throw err;
    }
  };

  const deleteAppointment = async (id: string) => {
    try {
      await axios.delete(`/api/appointments/${id}`);
      setAppointments(appointments.filter((appointment) => appointment.id !== id));
      addNotification({
        type: 'success',
        message: 'تم حذف الموعد بنجاح',
      });
    } catch (err) {
      addNotification({
        type: 'error',
        message: 'فشل في حذف الموعد',
      });
      throw err;
    }
  };

  const getAppointmentsByDate = (date: Date) => {
    return appointments.filter(
      (appointment) =>
        new Date(appointment.date).toDateString() === date.toDateString()
    );
  };

  const getAppointmentsByPatient = (patientId: string) => {
    return appointments.filter(
      (appointment) => appointment.patientName === patientId
    );
  };

  const getAppointmentStats = () => {
    const total = appointments.length;
    const completed = appointments.filter(
      (appointment) => appointment.status === 'completed'
    ).length;
    const cancelled = appointments.filter(
      (appointment) => appointment.status === 'cancelled'
    ).length;
    const scheduled = appointments.filter(
      (appointment) => appointment.status === 'scheduled'
    ).length;

    return {
      total,
      completed,
      cancelled,
      scheduled,
    };
  };

  return {
    appointments,
    loading,
    error,
    addAppointment,
    updateAppointment,
    deleteAppointment,
    getAppointmentsByDate,
    getAppointmentsByPatient,
    getAppointmentStats,
    refreshAppointments: fetchAppointments,
  };
};

export default useSchedule;

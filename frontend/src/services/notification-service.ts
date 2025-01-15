import { useState, useCallback, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { io, Socket } from 'socket.io-client';

export interface Notification {
  id: number;
  type: string;
  recipientId: number;
  data: any;
  read: boolean;
  createdAt: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || '';
const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || '';

export function useNotificationService() {
  const { getAuthHeaders, user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [socket, setSocket] = useState<Socket | null>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);

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

  // إعداد اتصال Socket.IO
  useEffect(() => {
    if (user) {
      const newSocket = io(SOCKET_URL, {
        auth: {
          token: getAuthHeaders().Authorization,
        },
      });

      newSocket.on('connect', () => {
        console.log('Connected to notification server');
      });

      newSocket.on('notification', (notification: Notification) => {
        setNotifications((prev) => [notification, ...prev]);
        // عرض إشعار للمستخدم
        if (Notification.permission === 'granted') {
          new Notification(getNotificationTitle(notification), {
            body: getNotificationBody(notification),
            icon: '/logo192.png',
          });
        }
      });

      setSocket(newSocket);

      return () => {
        newSocket.disconnect();
      };
    }
  }, [user]);

  const getNotificationTitle = (notification: Notification) => {
    switch (notification.type) {
      case 'high_risk_diagnosis':
        return 'تنبيه: تشخيص عالي الخطورة';
      case 'follow_up_reminder':
        return 'تذكير بموعد المتابعة';
      case 'reminder_update':
        return 'تحديث في التذكير';
      default:
        return 'إشعار جديد';
    }
  };

  const getNotificationBody = (notification: Notification) => {
    switch (notification.type) {
      case 'high_risk_diagnosis':
        return `المريض ${notification.data.patientName} لديه تشخيص يحتاج إلى اهتمام فوري`;
      case 'follow_up_reminder':
        return `موعد متابعة قادم في ${new Date(notification.data.datetime).toLocaleString('ar-SA')}`;
      case 'reminder_update':
        return `تم تحديث تذكير: ${notification.data.title}`;
      default:
        return JSON.stringify(notification.data);
    }
  };

  const sendNotification = useCallback(async (notification: {
    type: string;
    recipientId: number;
    data: any;
  }) => {
    return handleRequest(
      axios.post<Notification>(
        `${API_BASE_URL}/api/notifications/`,
        notification,
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const getNotifications = useCallback(async () => {
    return handleRequest(
      axios.get<Notification[]>(
        `${API_BASE_URL}/api/notifications/`,
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const markAsRead = useCallback(async (notificationId: number) => {
    return handleRequest(
      axios.patch<Notification>(
        `${API_BASE_URL}/api/notifications/${notificationId}/read/`,
        {},
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const markAllAsRead = useCallback(async () => {
    return handleRequest(
      axios.patch<void>(
        `${API_BASE_URL}/api/notifications/mark-all-read/`,
        {},
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const deleteNotification = useCallback(async (notificationId: number) => {
    return handleRequest(
      axios.delete(
        `${API_BASE_URL}/api/notifications/${notificationId}/`,
        { headers: getAuthHeaders() }
      )
    );
  }, [getAuthHeaders, handleRequest]);

  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    }
    return false;
  };

  return {
    loading,
    error,
    notifications,
    sendNotification,
    getNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    requestNotificationPermission,
  };
}

import { useEffect, useRef } from 'react';
import io, { Socket } from 'socket.io-client';
import { useAuth } from './useAuth';

export const useSocket = () => {
  const { user, isAuthenticated } = useAuth();
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    if (isAuthenticated && user) {
      // إنشاء اتصال السوكيت
      socketRef.current = io(process.env.REACT_APP_SOCKET_URL || 'http://localhost:8000', {
        auth: {
          token: localStorage.getItem('token')
        },
        query: {
          userId: user.id,
          role: user.role
        }
      });

      // معالجة أحداث الاتصال
      socketRef.current.on('connect', () => {
        console.log('Socket connected');
      });

      socketRef.current.on('connect_error', (error) => {
        console.error('Socket connection error:', error);
      });

      socketRef.current.on('disconnect', (reason) => {
        console.log('Socket disconnected:', reason);
      });

      // تنظيف عند إزالة المكون
      return () => {
        if (socketRef.current) {
          socketRef.current.disconnect();
          socketRef.current = null;
        }
      };
    }
  }, [isAuthenticated, user]);

  return socketRef.current;
};

export default useSocket;

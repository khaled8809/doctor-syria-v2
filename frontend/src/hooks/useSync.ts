import { useState, useEffect } from 'react';
import { useSocket } from './useSocket';
import { useDashboard } from '../components/dashboard/integration/DashboardIntegration';

interface SyncOptions {
  interval?: number;
  autoSync?: boolean;
  retryOnError?: boolean;
  maxRetries?: number;
}

interface SyncState {
  lastSync: Date | null;
  syncing: boolean;
  error: Error | null;
  retryCount: number;
}

export const useSync = (options: SyncOptions = {}) => {
  const {
    interval = 60000, // تحديث كل دقيقة افتراضياً
    autoSync = true,
    retryOnError = true,
    maxRetries = 3
  } = options;

  const socket = useSocket();
  const { refreshData, state, updateState } = useDashboard();
  const [syncState, setSyncState] = useState<SyncState>({
    lastSync: null,
    syncing: false,
    error: null,
    retryCount: 0
  });

  // وظيفة المزامنة
  const sync = async () => {
    if (syncState.syncing) return;

    try {
      setSyncState(prev => ({ ...prev, syncing: true, error: null }));

      // تحديث البيانات
      await refreshData();

      // إرسال حالة المزامنة للخادم
      socket?.emit('sync_status', {
        clientTime: new Date(),
        lastSync: syncState.lastSync,
        userId: state.currentUser?.id
      });

      setSyncState(prev => ({
        ...prev,
        lastSync: new Date(),
        syncing: false,
        retryCount: 0
      }));

    } catch (error) {
      console.error('Sync error:', error);
      
      setSyncState(prev => ({
        ...prev,
        syncing: false,
        error: error as Error,
        retryCount: prev.retryCount + 1
      }));

      // إعادة المحاولة إذا كان مسموحاً
      if (retryOnError && syncState.retryCount < maxRetries) {
        setTimeout(sync, 5000); // إعادة المحاولة بعد 5 ثوانٍ
      }
    }
  };

  // إعداد المزامنة التلقائية
  useEffect(() => {
    if (autoSync) {
      sync();
      const intervalId = setInterval(sync, interval);

      return () => clearInterval(intervalId);
    }
  }, [autoSync, interval]);

  // الاستماع لأحداث المزامنة
  useEffect(() => {
    if (socket) {
      socket.on('sync_required', () => {
        sync();
      });

      socket.on('data_update', (updates: any) => {
        updateState(updates);
      });

      return () => {
        socket.off('sync_required');
        socket.off('data_update');
      };
    }
  }, [socket]);

  // مراقبة حالة الاتصال
  useEffect(() => {
    const handleOnline = () => {
      console.log('Connection restored - syncing data...');
      sync();
    };

    window.addEventListener('online', handleOnline);

    return () => {
      window.removeEventListener('online', handleOnline);
    };
  }, []);

  return {
    sync,
    syncState,
    resetSync: () => setSyncState({
      lastSync: null,
      syncing: false,
      error: null,
      retryCount: 0
    })
  };
};

export default useSync;

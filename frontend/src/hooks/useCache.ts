import { useState, useCallback, useRef, useEffect } from 'react';

interface CacheOptions {
  ttl?: number; // Time to live in milliseconds
  maxSize?: number; // Maximum number of items in cache
  persistKey?: string; // Key for persistent storage
}

interface CacheItem<T> {
  value: T;
  timestamp: number;
}

interface CacheStats {
  hits: number;
  misses: number;
  size: number;
  oldestKey?: string;
  newestKey?: string;
}

export function useCache<T>(options: CacheOptions = {}) {
  const {
    ttl = 5 * 60 * 1000, // 5 minutes default
    maxSize = 100,
    persistKey,
  } = options;

  // استخدام useRef للحفاظ على مرجع ثابت للكاش
  const cacheRef = useRef<Map<string, CacheItem<T>>>(new Map());
  const statsRef = useRef<CacheStats>({
    hits: 0,
    misses: 0,
    size: 0,
  });

  // تحميل البيانات المحفوظة عند التهيئة
  useEffect(() => {
    if (persistKey) {
      try {
        const stored = localStorage.getItem(persistKey);
        if (stored) {
          const { cache, stats } = JSON.parse(stored);
          cacheRef.current = new Map(Object.entries(cache));
          statsRef.current = stats;
        }
      } catch (error) {
        console.error('Error loading cache from storage:', error);
      }
    }
  }, [persistKey]);

  // حفظ البيانات عند التغيير
  const persistCache = useCallback(() => {
    if (persistKey) {
      try {
        const cache = Object.fromEntries(cacheRef.current.entries());
        localStorage.setItem(
          persistKey,
          JSON.stringify({
            cache,
            stats: statsRef.current,
          })
        );
      } catch (error) {
        console.error('Error persisting cache:', error);
      }
    }
  }, [persistKey]);

  // تنظيف الكاش القديم
  const cleanup = useCallback(() => {
    const now = Date.now();
    let removed = 0;

    // إزالة العناصر منتهية الصلاحية
    for (const [key, item] of cacheRef.current.entries()) {
      if (now - item.timestamp > ttl) {
        cacheRef.current.delete(key);
        removed++;
      }
    }

    // إزالة العناصر الزائدة عن الحد الأقصى
    if (cacheRef.current.size > maxSize) {
      const sortedEntries = Array.from(cacheRef.current.entries())
        .sort(([, a], [, b]) => a.timestamp - b.timestamp);

      const toRemove = cacheRef.current.size - maxSize;
      for (let i = 0; i < toRemove; i++) {
        const [key] = sortedEntries[i];
        cacheRef.current.delete(key);
        removed++;
      }
    }

    if (removed > 0) {
      statsRef.current.size = cacheRef.current.size;
      persistCache();
    }
  }, [ttl, maxSize, persistCache]);

  // تحديث إحصائيات الكاش
  const updateStats = useCallback(() => {
    const entries = Array.from(cacheRef.current.entries());
    if (entries.length > 0) {
      const sorted = entries.sort(([, a], [, b]) => a.timestamp - b.timestamp);
      statsRef.current = {
        ...statsRef.current,
        size: cacheRef.current.size,
        oldestKey: sorted[0][0],
        newestKey: sorted[sorted.length - 1][0],
      };
    }
  }, []);

  // وضع قيمة في الكاش
  const set = useCallback((key: string, value: T) => {
    cleanup();
    cacheRef.current.set(key, {
      value,
      timestamp: Date.now(),
    });
    updateStats();
    persistCache();
  }, [cleanup, updateStats, persistCache]);

  // الحصول على قيمة من الكاش
  const get = useCallback((key: string): T | undefined => {
    const item = cacheRef.current.get(key);
    
    if (!item) {
      statsRef.current.misses++;
      return undefined;
    }

    if (Date.now() - item.timestamp > ttl) {
      cacheRef.current.delete(key);
      statsRef.current.misses++;
      updateStats();
      persistCache();
      return undefined;
    }

    statsRef.current.hits++;
    return item.value;
  }, [ttl, updateStats, persistCache]);

  // حذف قيمة من الكاش
  const remove = useCallback((key: string) => {
    const deleted = cacheRef.current.delete(key);
    if (deleted) {
      updateStats();
      persistCache();
    }
    return deleted;
  }, [updateStats, persistCache]);

  // تفريغ الكاش
  const clear = useCallback(() => {
    cacheRef.current.clear();
    statsRef.current = {
      hits: 0,
      misses: 0,
      size: 0,
    };
    persistCache();
  }, [persistCache]);

  // الحصول على إحصائيات الكاش
  const getStats = useCallback((): CacheStats => {
    return { ...statsRef.current };
  }, []);

  return {
    get,
    set,
    remove,
    clear,
    getStats,
  };
}

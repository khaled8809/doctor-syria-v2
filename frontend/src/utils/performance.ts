import { useCallback, useEffect, useRef } from 'react';

// قياس وقت التحميل للمكونات
export const useComponentLoadTime = (componentName: string) => {
  const startTime = useRef(performance.now());

  useEffect(() => {
    const endTime = performance.now();
    const loadTime = endTime - startTime.current;
    console.debug(`[Performance] ${componentName} loaded in ${loadTime.toFixed(2)}ms`);
  }, [componentName]);
};

// تأخير التحميل للمكونات غير المرئية
export const useLazyLoading = (isVisible: boolean) => {
  const [shouldLoad, setShouldLoad] = useState(false);

  useEffect(() => {
    if (isVisible && !shouldLoad) {
      setShouldLoad(true);
    }
  }, [isVisible]);

  return shouldLoad;
};

// تحسين الأداء للقوائم الطويلة
export const useVirtualization = <T>(
  items: T[],
  itemHeight: number,
  containerHeight: number
) => {
  const [visibleItems, setVisibleItems] = useState<T[]>([]);
  const [startIndex, setStartIndex] = useState(0);

  const handleScroll = useCallback(
    (scrollTop: number) => {
      const start = Math.floor(scrollTop / itemHeight);
      const visibleCount = Math.ceil(containerHeight / itemHeight);
      const end = Math.min(start + visibleCount + 1, items.length);

      setStartIndex(start);
      setVisibleItems(items.slice(start, end));
    },
    [items, itemHeight, containerHeight]
  );

  return {
    visibleItems,
    startIndex,
    totalHeight: items.length * itemHeight,
    handleScroll,
  };
};

// تحسين الأداء للجداول
export const useTableOptimization = <T>(
  data: T[],
  pageSize: number,
  sortConfig?: { key: keyof T; direction: 'asc' | 'desc' }
) => {
  const [processedData, setProcessedData] = useState<T[]>([]);
  const previousData = useRef<T[]>([]);
  const previousSort = useRef(sortConfig);

  useEffect(() => {
    const shouldUpdate =
      data !== previousData.current ||
      JSON.stringify(sortConfig) !== JSON.stringify(previousSort.current);

    if (shouldUpdate) {
      const worker = new Worker(new URL('./tableWorker.ts', import.meta.url));

      worker.postMessage({ data, sortConfig });

      worker.onmessage = (event) => {
        setProcessedData(event.data);
        previousData.current = data;
        previousSort.current = sortConfig;
      };

      return () => worker.terminate();
    }
  }, [data, sortConfig]);

  return processedData;
};

// تحسين أداء الرسوم البيانية
export const useChartOptimization = (data: any[], threshold: number = 1000) => {
  const optimizeData = useCallback(
    (rawData: any[]) => {
      if (rawData.length <= threshold) return rawData;

      const factor = Math.ceil(rawData.length / threshold);
      return rawData.filter((_, index) => index % factor === 0);
    },
    [threshold]
  );

  return optimizeData(data);
};

// تخزين مؤقت للبيانات
export const useDataCache = <T>(key: string, data: T, ttl: number = 5 * 60 * 1000) => {
  const cache = useRef(new Map<string, { data: T; timestamp: number }>());

  const getCachedData = useCallback(() => {
    const cached = cache.current.get(key);
    if (!cached) return null;

    const now = Date.now();
    if (now - cached.timestamp > ttl) {
      cache.current.delete(key);
      return null;
    }

    return cached.data;
  }, [key, ttl]);

  const setCachedData = useCallback(
    (newData: T) => {
      cache.current.set(key, { data: newData, timestamp: Date.now() });
    },
    [key]
  );

  useEffect(() => {
    setCachedData(data);
  }, [data, setCachedData]);

  return {
    getCachedData,
    setCachedData,
  };
};

// تحسين أداء التحديثات المتكررة
export const useDebounceUpdate = <T>(value: T, delay: number = 300) => {
  const [debouncedValue, setDebouncedValue] = useState(value);
  const timeoutRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    timeoutRef.current = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [value, delay]);

  return debouncedValue;
};

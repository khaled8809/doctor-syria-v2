import { useEffect, useRef, useCallback, useState } from 'react';

interface PerformanceMetrics {
  fps: number;
  memory: {
    usedJSHeapSize: number;
    totalJSHeapSize: number;
    jsHeapSizeLimit: number;
  };
  timing: {
    loadTime: number;
    domContentLoaded: number;
    firstPaint: number;
    firstContentfulPaint: number;
  };
  resources: {
    count: number;
    size: number;
  };
}

interface PerformanceOptions {
  enableFPS?: boolean;
  enableMemory?: boolean;
  enableTiming?: boolean;
  enableResources?: boolean;
  sampleInterval?: number;
  warningThresholds?: {
    fps?: number;
    memory?: number;
    loadTime?: number;
  };
}

export function usePerformance(options: PerformanceOptions = {}) {
  const {
    enableFPS = true,
    enableMemory = true,
    enableTiming = true,
    enableResources = true,
    sampleInterval = 1000,
    warningThresholds = {
      fps: 30,
      memory: 0.9, // 90% of heap size
      loadTime: 3000, // 3 seconds
    },
  } = options;

  const [metrics, setMetrics] = useState<PerformanceMetrics>({
    fps: 0,
    memory: {
      usedJSHeapSize: 0,
      totalJSHeapSize: 0,
      jsHeapSizeLimit: 0,
    },
    timing: {
      loadTime: 0,
      domContentLoaded: 0,
      firstPaint: 0,
      firstContentfulPaint: 0,
    },
    resources: {
      count: 0,
      size: 0,
    },
  });

  const frameCountRef = useRef(0);
  const lastFrameTimeRef = useRef(performance.now());
  const rafIdRef = useRef<number>();
  const intervalIdRef = useRef<NodeJS.Timeout>();

  // قياس معدل الإطارات
  const measureFPS = useCallback(() => {
    const now = performance.now();
    frameCountRef.current++;

    if (now - lastFrameTimeRef.current >= 1000) {
      setMetrics((prev) => ({
        ...prev,
        fps: frameCountRef.current,
      }));

      frameCountRef.current = 0;
      lastFrameTimeRef.current = now;
    }

    rafIdRef.current = requestAnimationFrame(measureFPS);
  }, []);

  // قياس استخدام الذاكرة
  const measureMemory = useCallback(async () => {
    if ('memory' in performance) {
      const memory = (performance as any).memory;
      setMetrics((prev) => ({
        ...prev,
        memory: {
          usedJSHeapSize: memory.usedJSHeapSize,
          totalJSHeapSize: memory.totalJSHeapSize,
          jsHeapSizeLimit: memory.jsHeapSizeLimit,
        },
      }));
    }
  }, []);

  // قياس توقيتات الصفحة
  const measureTiming = useCallback(() => {
    const timing = performance.timing;
    const paintEntries = performance.getEntriesByType('paint');

    const firstPaint = paintEntries.find((entry) => entry.name === 'first-paint')?.startTime || 0;
    const firstContentfulPaint = paintEntries.find(
      (entry) => entry.name === 'first-contentful-paint'
    )?.startTime || 0;

    setMetrics((prev) => ({
      ...prev,
      timing: {
        loadTime: timing.loadEventEnd - timing.navigationStart,
        domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
        firstPaint,
        firstContentfulPaint,
      },
    }));
  }, []);

  // قياس الموارد
  const measureResources = useCallback(() => {
    const resources = performance.getEntriesByType('resource');
    const totalSize = resources.reduce((acc, resource) => acc + (resource as any).encodedBodySize, 0);

    setMetrics((prev) => ({
      ...prev,
      resources: {
        count: resources.length,
        size: totalSize,
      },
    }));
  }, []);

  // تحسين الأداء تلقائياً
  const optimizePerformance = useCallback(() => {
    // تحسين معدل الإطارات
    if (metrics.fps < (warningThresholds.fps || 30)) {
      console.warn('Low FPS detected. Consider reducing animations or DOM updates.');
    }

    // تحسين استخدام الذاكرة
    if (metrics.memory.usedJSHeapSize / metrics.memory.jsHeapSizeLimit > (warningThresholds.memory || 0.9)) {
      console.warn('High memory usage detected. Consider cleaning up unused objects.');
    }

    // تحسين وقت التحميل
    if (metrics.timing.loadTime > (warningThresholds.loadTime || 3000)) {
      console.warn('Slow page load detected. Consider optimizing resource loading.');
    }
  }, [metrics, warningThresholds]);

  // تنظيف الأداء
  const cleanup = useCallback(() => {
    if (rafIdRef.current) {
      cancelAnimationFrame(rafIdRef.current);
    }
    if (intervalIdRef.current) {
      clearInterval(intervalIdRef.current);
    }
  }, []);

  // بدء القياس
  useEffect(() => {
    if (enableFPS) {
      measureFPS();
    }

    intervalIdRef.current = setInterval(() => {
      if (enableMemory) {
        measureMemory();
      }
      if (enableTiming) {
        measureTiming();
      }
      if (enableResources) {
        measureResources();
      }
      optimizePerformance();
    }, sampleInterval);

    return cleanup;
  }, [
    enableFPS,
    enableMemory,
    enableTiming,
    enableResources,
    sampleInterval,
    measureFPS,
    measureMemory,
    measureTiming,
    measureResources,
    optimizePerformance,
    cleanup,
  ]);

  // تنسيق حجم الملف
  const formatSize = (bytes: number): string => {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }

    return `${size.toFixed(2)} ${units[unitIndex]}`;
  };

  return {
    metrics,
    formatSize,
    cleanup,
  };
}

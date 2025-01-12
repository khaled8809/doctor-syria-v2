import { useState, useCallback, useRef, useEffect } from 'react';
import { useCache } from './useCache';
import axios, { AxiosRequestConfig, AxiosResponse, CancelToken } from 'axios';

interface RequestOptions extends AxiosRequestConfig {
  cacheKey?: string;
  cacheTTL?: number;
  retryCount?: number;
  retryDelay?: number;
  timeout?: number;
  onUploadProgress?: (progress: number) => void;
  onDownloadProgress?: (progress: number) => void;
}

interface RequestState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  progress: number;
}

export function useRequest<T>(defaultOptions?: RequestOptions) {
  const cache = useCache<T>({
    ttl: defaultOptions?.cacheTTL || 5 * 60 * 1000, // 5 minutes
    maxSize: 100,
  });

  const [state, setState] = useState<RequestState<T>>({
    data: null,
    loading: false,
    error: null,
    progress: 0,
  });

  const cancelTokenRef = useRef<CancelToken>();
  const activeRequestsRef = useRef<Map<string, Promise<AxiosResponse<T>>>>(new Map());

  // تنظيف عند إزالة المكون
  useEffect(() => {
    return () => {
      if (cancelTokenRef.current) {
        axios.Cancel;
      }
    };
  }, []);

  const executeRequest = useCallback(async (
    url: string,
    options: RequestOptions = {}
  ): Promise<T> => {
    const {
      cacheKey,
      cacheTTL,
      retryCount = 3,
      retryDelay = 1000,
      timeout = 30000,
      onUploadProgress,
      onDownloadProgress,
      ...axiosOptions
    } = options;

    // التحقق من الكاش
    if (cacheKey) {
      const cachedData = cache.get(cacheKey);
      if (cachedData) {
        setState({
          data: cachedData,
          loading: false,
          error: null,
          progress: 100,
        });
        return cachedData;
      }
    }

    // إلغاء الطلب السابق إذا وجد
    if (cancelTokenRef.current) {
      axios.Cancel;
    }

    // إنشاء توكن إلغاء جديد
    const source = axios.CancelToken.source();
    cancelTokenRef.current = source.token;

    // التحقق من الطلبات النشطة
    const activeRequestKey = JSON.stringify({ url, ...axiosOptions });
    if (activeRequestsRef.current.has(activeRequestKey)) {
      return (await activeRequestsRef.current.get(activeRequestKey))?.data;
    }

    setState((prev) => ({ ...prev, loading: true, error: null }));

    const makeRequest = async (retryAttempt: number = 0): Promise<T> => {
      try {
        const request = axios({
          url,
          ...axiosOptions,
          timeout,
          cancelToken: source.token,
          onUploadProgress: (e) => {
            const progress = Math.round((e.loaded * 100) / (e.total || 0));
            setState((prev) => ({ ...prev, progress }));
            onUploadProgress?.(progress);
          },
          onDownloadProgress: (e) => {
            const progress = Math.round((e.loaded * 100) / (e.total || 0));
            setState((prev) => ({ ...prev, progress }));
            onDownloadProgress?.(progress);
          },
        });

        activeRequestsRef.current.set(activeRequestKey, request);

        const response = await request;
        const data = response.data;

        // تخزين في الكاش
        if (cacheKey) {
          cache.set(cacheKey, data);
        }

        setState({
          data,
          loading: false,
          error: null,
          progress: 100,
        });

        return data;
      } catch (error: any) {
        // إعادة المحاولة في حالة الفشل
        if (
          retryAttempt < retryCount &&
          error.code !== 'ECONNABORTED' &&
          !axios.isCancel(error)
        ) {
          await new Promise((resolve) => setTimeout(resolve, retryDelay));
          return makeRequest(retryAttempt + 1);
        }

        setState({
          data: null,
          loading: false,
          error,
          progress: 0,
        });

        throw error;
      } finally {
        activeRequestsRef.current.delete(activeRequestKey);
      }
    };

    return makeRequest();
  }, [cache]);

  const cancelRequest = useCallback(() => {
    if (cancelTokenRef.current) {
      axios.Cancel;
      setState({
        data: null,
        loading: false,
        error: new Error('Request cancelled'),
        progress: 0,
      });
    }
  }, []);

  const clearCache = useCallback(() => {
    cache.clear();
  }, [cache]);

  return {
    ...state,
    executeRequest,
    cancelRequest,
    clearCache,
  };
}

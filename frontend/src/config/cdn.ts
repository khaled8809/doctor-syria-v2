export const CDN_URL = process.env.REACT_APP_CDN_URL || 'https://cdn.doctor-syria.com';

export const getImageUrl = (path: string, options?: {
  width?: number;
  height?: number;
  quality?: number;
  format?: 'webp' | 'jpeg' | 'png';
}) => {
  const url = new URL(`${CDN_URL}${path}`);

  if (options?.width) {
    url.searchParams.set('width', options.width.toString());
  }

  if (options?.height) {
    url.searchParams.set('height', options.height.toString());
  }

  if (options?.quality) {
    url.searchParams.set('quality', options.quality.toString());
  }

  if (options?.format) {
    url.searchParams.set('format', options.format);
  }

  return url.toString();
};

export const preloadImage = (path: string) => {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.as = 'image';
  link.href = getImageUrl(path);
  document.head.appendChild(link);
};

export const preloadCriticalImages = () => {
  const criticalImages = [
    '/logo.png',
    '/icons/dashboard.svg',
    '/icons/patients.svg',
    '/icons/appointments.svg',
  ];

  criticalImages.forEach(preloadImage);
};

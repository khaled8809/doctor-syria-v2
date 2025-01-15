import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface ImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  src: string;
  alt: string;
  fallback?: string;
  blur?: boolean;
  aspectRatio?: string;
  objectFit?: 'contain' | 'cover' | 'fill' | 'none' | 'scale-down';
  className?: string;
}

const Image = motion(({ src, alt, fallback = '/images/placeholder.png', blur = true, aspectRatio = '1/1', objectFit = 'cover', className = '', ...props }: ImageProps) => {
  const [loaded, setLoaded] = React.useState(false);
  const [error, setError] = React.useState(false);

  const handleLoad = () => {
    setLoaded(true);
  };

  const handleError = () => {
    setError(true);
  };

  return (
    <div
      className={`relative overflow-hidden ${className}`}
      style={{ aspectRatio }}
    >
      <AnimatePresence>
        {blur && (
          <motion.div
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-gray-200 animate-pulse"
          />
        )}
      </AnimatePresence>

      <img
        src={error ? fallback : src}
        alt={alt}
        className={`${className} ${loaded ? 'opacity-100' : 'opacity-0'} ${objectFit} ${blur && loaded ? 'blur-sm scale-105' : 'blur-0 scale-100'}`}
        onLoad={handleLoad}
        onError={handleError}
        {...props}
      />

      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
          <span className="text-gray-400">
            {alt || 'صورة غير متوفرة'}
          </span>
        </div>
      )}
    </div>
  );
});

export default Image;

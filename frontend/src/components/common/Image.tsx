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

const Image: React.FC<ImageProps> = ({
  src,
  alt,
  fallback = '/images/placeholder.png',
  blur = true,
  aspectRatio = '1/1',
  objectFit = 'cover',
  className = '',
  ...props
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);
  const [currentSrc, setCurrentSrc] = useState(src);

  useEffect(() => {
    setCurrentSrc(src);
    setIsLoading(true);
    setError(false);
  }, [src]);

  const handleLoad = () => {
    setIsLoading(false);
  };

  const handleError = () => {
    setError(true);
    setCurrentSrc(fallback);
  };

  // Generate srcSet for responsive images
  const generateSrcSet = (url: string) => {
    const sizes = [320, 480, 640, 768, 1024, 1280];
    return sizes
      .map((size) => {
        const imageUrl = new URL(url);
        imageUrl.searchParams.set('width', size.toString());
        return `${imageUrl.toString()} ${size}w`;
      })
      .join(', ');
  };

  return (
    <div
      className={`relative overflow-hidden ${className}`}
      style={{ aspectRatio }}
    >
      <AnimatePresence>
        {isLoading && blur && (
          <motion.div
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-gray-200 animate-pulse"
          />
        )}
      </AnimatePresence>

      <motion.img
        {...props}
        src={currentSrc}
        alt={alt}
        srcSet={generateSrcSet(currentSrc)}
        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
        loading="lazy"
        decoding="async"
        onLoad={handleLoad}
        onError={handleError}
        initial={{ opacity: 0 }}
        animate={{ opacity: isLoading ? 0.5 : 1 }}
        transition={{ duration: 0.3 }}
        className={`w-full h-full ${objectFit} ${
          isLoading && blur ? 'blur-sm scale-105' : 'blur-0 scale-100'
        }`}
        style={{ objectFit }}
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
};

export default Image;

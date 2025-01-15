import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
  variant?: 'contained' | 'outlined' | 'text';
  color?: 'primary' | 'secondary' | 'error' | 'warning' | 'info' | 'success';
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
}

const Button: React.FC<ButtonProps> = motion((
  {
    children,
    loading,
    variant = 'contained',
    color = 'primary',
    startIcon,
    endIcon,
    className = '',
    ...props
  }: ButtonProps
) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-md focus:outline-none transition-colors duration-200';

  const variants = {
    contained: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-2 focus:ring-offset-2 focus:ring-primary-500',
    outlined: 'border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-2 focus:ring-offset-2 focus:ring-primary-500',
    text: 'text-gray-700 hover:text-gray-900 focus:ring-2 focus:ring-offset-2 focus:ring-primary-500',
  };

  const colors = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-2 focus:ring-offset-2 focus:ring-primary-500',
    secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-2 focus:ring-offset-2 focus:ring-secondary-500',
    error: 'bg-error-600 text-white hover:bg-error-700 focus:ring-2 focus:ring-offset-2 focus:ring-error-500',
    warning: 'bg-warning-600 text-white hover:bg-warning-700 focus:ring-2 focus:ring-offset-2 focus:ring-warning-500',
    info: 'bg-info-600 text-white hover:bg-info-700 focus:ring-2 focus:ring-offset-2 focus:ring-info-500',
    success: 'bg-success-600 text-white hover:bg-success-700 focus:ring-2 focus:ring-offset-2 focus:ring-success-500',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <motion.button
      whileTap={{ scale: 0.98 }}
      className={`${baseStyles} ${variants[variant]} ${colors[color]} ${sizes['md']} ${className}`}
      disabled={loading}
      {...props}
    >
      {loading ? (
        <svg
          className="w-5 h-5 mr-3 -ml-1 animate-spin"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      ) : startIcon ? (
        <span className="mr-2">{startIcon}</span>
      ) : null}
      {children}
      {endIcon ? (
        <span className="ml-2">{endIcon}</span>
      ) : null}
    </motion.button>
  );
});

export default Button;

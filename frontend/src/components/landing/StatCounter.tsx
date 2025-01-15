import React from 'react';
import { Typography, Box } from '@mui/material';
import { motion, useAnimation } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

interface StatCounterProps {
  number: string;
  label: string;
}

const StatCounter: React.FC<StatCounterProps> = ({ number, label }) => {
  const controls = useAnimation();
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.2,
  });

  React.useEffect(() => {
    if (inView) {
      controls.start({
        scale: [0.5, 1.2, 1],
        opacity: [0, 1],
        transition: {
          duration: 0.8,
          ease: 'easeOut',
        },
      });
    }
  }, [controls, inView]);

  return (
    <motion.div ref={ref} animate={controls} initial={{ opacity: 0, scale: 0.5 }}>
      <Box textAlign="center">
        <Typography
          variant="h3"
          component="div"
          color="primary"
          gutterBottom
          sx={{ fontWeight: 'bold' }}
        >
          {number}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          {label}
        </Typography>
      </Box>
    </motion.div>
  );
};

export default StatCounter;

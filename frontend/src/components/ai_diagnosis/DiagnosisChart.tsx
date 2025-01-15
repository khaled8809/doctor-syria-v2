import React from 'react';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Tooltip,
  Legend,
} from 'recharts';
import { Box, Typography, useTheme } from '@mui/material';

interface DiagnosisChartProps {
  data: {
    disease: {
      name: string;
      risk_level: number;
    };
    confidence: number;
    reasoning: {
      matching_symptoms: Array<{
        name: string;
        importance: number;
      }>;
    };
  }[];
}

export default function DiagnosisChart({ data }: DiagnosisChartProps) {
  const theme = useTheme();

  // تحويل البيانات إلى تنسيق مناسب للرسم البياني
  const chartData = data.map((result) => {
    const matchingSymptoms = result.reasoning.matching_symptoms.reduce(
      (acc, symptom) => acc + symptom.importance,
      0
    );

    return {
      name: result.disease.name,
      confidence: result.confidence,
      symptoms: matchingSymptoms,
      risk: result.disease.risk_level * 33.33, // تحويل مستوى الخطر إلى نسبة مئوية
    };
  });

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <Box
          sx={{
            bgcolor: 'background.paper',
            p: 2,
            border: 1,
            borderColor: 'divider',
            borderRadius: 1,
          }}
        >
          <Typography variant="subtitle2" gutterBottom>
            {data.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            نسبة الثقة: {data.confidence}%
          </Typography>
          <Typography variant="body2" color="text.secondary">
            مستوى الخطر: {Math.round(data.risk / 33.33)}/3
          </Typography>
        </Box>
      );
    }
    return null;
  };

  return (
    <Box sx={{ width: '100%', height: 400, mt: 4 }}>
      <Typography variant="h6" gutterBottom align="center">
        تحليل النتائج
      </Typography>
      <ResponsiveContainer>
        <RadarChart data={chartData}>
          <PolarGrid />
          <PolarAngleAxis
            dataKey="name"
            tick={{ fill: theme.palette.text.primary }}
          />
          <PolarRadiusAxis
            angle={30}
            domain={[0, 100]}
            tick={{ fill: theme.palette.text.secondary }}
          />
          <Radar
            name="نسبة الثقة"
            dataKey="confidence"
            stroke={theme.palette.primary.main}
            fill={theme.palette.primary.main}
            fillOpacity={0.5}
          />
          <Radar
            name="مستوى الخطر"
            dataKey="risk"
            stroke={theme.palette.error.main}
            fill={theme.palette.error.main}
            fillOpacity={0.5}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </Box>
  );
}

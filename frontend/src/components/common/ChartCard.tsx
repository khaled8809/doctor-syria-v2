import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  IconButton,
  Menu,
  MenuItem,
  Box,
  Typography,
  useTheme,
  Skeleton,
  Tooltip,
} from '@mui/material';
import {
  MoreVert as MoreVertIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
} from 'recharts';

type ChartType = 'line' | 'bar' | 'area' | 'pie';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  data: any[];
  type?: ChartType;
  dataKey: string;
  categories?: string[];
  loading?: boolean;
  error?: string;
  height?: number;
  onRefresh?: () => void;
  onDownload?: (format: 'png' | 'svg') => void;
  info?: string;
  customColors?: string[];
  stacked?: boolean;
  showGrid?: boolean;
  showLegend?: boolean;
  xAxisLabel?: string;
  yAxisLabel?: string;
}

export default function ChartCard({
  title,
  subtitle,
  data,
  type = 'line',
  dataKey,
  categories = [],
  loading = false,
  error,
  height = 300,
  onRefresh,
  onDownload,
  info,
  customColors,
  stacked = false,
  showGrid = true,
  showLegend = true,
  xAxisLabel,
  yAxisLabel,
}: ChartCardProps) {
  const theme = useTheme();
  const [menuAnchor, setMenuAnchor] = useState<null | HTMLElement>(null);

  const defaultColors = [
    theme.palette.primary.main,
    theme.palette.secondary.main,
    theme.palette.tertiary.main,
    theme.palette.error.main,
    theme.palette.warning.main,
    theme.palette.info.main,
    theme.palette.success.main,
  ];

  const colors = customColors || defaultColors;

  const handleMenuOpen = (event: React.MouseEvent<HTMLButtonElement>) => {
    setMenuAnchor(event.currentTarget);
  };

  const handleMenuClose = () => {
    setMenuAnchor(null);
  };

  const renderChart = () => {
    const commonProps = {
      data,
      margin: { top: 10, right: 30, left: 0, bottom: 0 },
    };

    const commonAxisProps = {
      stroke: theme.palette.text.secondary,
      style: {
        fontSize: 12,
      },
    };

    switch (type) {
      case 'line':
        return (
          <LineChart {...commonProps}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />}
            <XAxis
              dataKey={dataKey}
              {...commonAxisProps}
              label={xAxisLabel ? { value: xAxisLabel, position: 'bottom' } : undefined}
            />
            <YAxis
              {...commonAxisProps}
              label={yAxisLabel ? { value: yAxisLabel, angle: -90, position: 'left' } : undefined}
            />
            <RechartsTooltip
              contentStyle={{
                backgroundColor: theme.palette.background.paper,
                border: `1px solid ${theme.palette.divider}`,
                borderRadius: 8,
              }}
            />
            {showLegend && <Legend />}
            {categories.map((category, index) => (
              <Line
                key={category}
                type="monotone"
                dataKey={category}
                stroke={colors[index % colors.length]}
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
            ))}
          </LineChart>
        );

      case 'bar':
        return (
          <BarChart {...commonProps}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />}
            <XAxis
              dataKey={dataKey}
              {...commonAxisProps}
              label={xAxisLabel ? { value: xAxisLabel, position: 'bottom' } : undefined}
            />
            <YAxis
              {...commonAxisProps}
              label={yAxisLabel ? { value: yAxisLabel, angle: -90, position: 'left' } : undefined}
            />
            <RechartsTooltip
              contentStyle={{
                backgroundColor: theme.palette.background.paper,
                border: `1px solid ${theme.palette.divider}`,
                borderRadius: 8,
              }}
            />
            {showLegend && <Legend />}
            {categories.map((category, index) => (
              <Bar
                key={category}
                dataKey={category}
                fill={colors[index % colors.length]}
                stackId={stacked ? 'stack' : undefined}
              />
            ))}
          </BarChart>
        );

      case 'area':
        return (
          <AreaChart {...commonProps}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />}
            <XAxis
              dataKey={dataKey}
              {...commonAxisProps}
              label={xAxisLabel ? { value: xAxisLabel, position: 'bottom' } : undefined}
            />
            <YAxis
              {...commonAxisProps}
              label={yAxisLabel ? { value: yAxisLabel, angle: -90, position: 'left' } : undefined}
            />
            <RechartsTooltip
              contentStyle={{
                backgroundColor: theme.palette.background.paper,
                border: `1px solid ${theme.palette.divider}`,
                borderRadius: 8,
              }}
            />
            {showLegend && <Legend />}
            {categories.map((category, index) => (
              <Area
                key={category}
                type="monotone"
                dataKey={category}
                fill={colors[index % colors.length]}
                stroke={colors[index % colors.length]}
                stackId={stacked ? 'stack' : undefined}
                fillOpacity={0.6}
              />
            ))}
          </AreaChart>
        );

      case 'pie':
        return (
          <PieChart>
            <Pie
              data={data}
              dataKey={categories[0]}
              nameKey={dataKey}
              cx="50%"
              cy="50%"
              outerRadius={80}
              label
            >
              {data.map((_, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <RechartsTooltip
              contentStyle={{
                backgroundColor: theme.palette.background.paper,
                border: `1px solid ${theme.palette.divider}`,
                borderRadius: 8,
              }}
            />
            {showLegend && <Legend />}
          </PieChart>
        );

      default:
        return null;
    }
  };

  return (
    <Card
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <CardHeader
        title={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              {title}
            </Typography>
            {info && (
              <Tooltip title={info}>
                <IconButton size="small">
                  <InfoIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            )}
          </Box>
        }
        subheader={subtitle}
        action={
          <>
            {onRefresh && (
              <IconButton onClick={onRefresh}>
                <RefreshIcon />
              </IconButton>
            )}
            {onDownload && (
              <IconButton onClick={handleMenuOpen}>
                <DownloadIcon />
              </IconButton>
            )}
            <IconButton onClick={handleMenuOpen}>
              <MoreVertIcon />
            </IconButton>
          </>
        }
      />

      <CardContent
        sx={{
          flexGrow: 1,
          minHeight: height,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {loading ? (
          <Box sx={{ width: '100%', height: '100%' }}>
            <Skeleton variant="rectangular" width="100%" height={height} />
          </Box>
        ) : error ? (
          <Typography color="error" align="center">
            {error}
          </Typography>
        ) : (
          <ResponsiveContainer width="100%" height={height}>
            {renderChart()}
          </ResponsiveContainer>
        )}
      </CardContent>

      <Menu
        anchorEl={menuAnchor}
        open={Boolean(menuAnchor)}
        onClose={handleMenuClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        {onDownload && (
          <>
            <MenuItem
              onClick={() => {
                onDownload('png');
                handleMenuClose();
              }}
            >
              تحميل كصورة PNG
            </MenuItem>
            <MenuItem
              onClick={() => {
                onDownload('svg');
                handleMenuClose();
              }}
            >
              تحميل كملف SVG
            </MenuItem>
          </>
        )}
        {onRefresh && (
          <MenuItem
            onClick={() => {
              onRefresh();
              handleMenuClose();
            }}
          >
            تحديث البيانات
          </MenuItem>
        )}
      </Menu>
    </Card>
  );
}

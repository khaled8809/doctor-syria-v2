import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Slider,
  Box,
  Radio,
  RadioGroup,
  Divider,
  useTheme,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { Area } from '../../types/area';

interface SearchFiltersProps {
  filters: {
    rating: number;
    availability: boolean;
    area: string;
  };
  areas: Area[];
  onFilterChange: (filters: any) => void;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({
  filters,
  areas,
  onFilterChange,
}) => {
  const { t } = useTranslation();
  const theme = useTheme();

  const handleRatingChange = (_: Event, value: number | number[]) => {
    onFilterChange({ ...filters, rating: value as number });
  };

  return (
    <Card elevation={1}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {t('filters.title')}
        </Typography>

        {/* تصفية حسب التقييم */}
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom>
            {t('filters.rating')}
          </Typography>
          <Slider
            value={filters.rating}
            onChange={handleRatingChange}
            min={0}
            max={5}
            step={0.5}
            marks
            valueLabelDisplay="auto"
            sx={{
              color: theme.palette.primary.main,
              '& .MuiSlider-valueLabel': {
                backgroundColor: theme.palette.primary.main,
              },
            }}
          />
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* تصفية حسب المنطقة */}
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom>
            {t('filters.area')}
          </Typography>
          <RadioGroup
            value={filters.area}
            onChange={(e) => onFilterChange({ ...filters, area: e.target.value })}
          >
            <FormControlLabel
              value=""
              control={<Radio />}
              label={t('filters.allAreas')}
            />
            {areas.map((area) => (
              <FormControlLabel
                key={area.id}
                value={area.id}
                control={<Radio />}
                label={area.name}
              />
            ))}
          </RadioGroup>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* خيارات إضافية */}
        <Box>
          <Typography gutterBottom>
            {t('filters.options')}
          </Typography>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox
                  checked={filters.availability}
                  onChange={(e) =>
                    onFilterChange({ ...filters, availability: e.target.checked })
                  }
                />
              }
              label={t('filters.availableNow')}
            />
          </FormGroup>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SearchFilters;

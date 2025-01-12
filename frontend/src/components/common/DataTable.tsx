import React, { useState, useMemo } from 'react';
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  TableSortLabel,
  Paper,
  TextField,
  IconButton,
  Tooltip,
  Checkbox,
  Typography,
  Chip,
  Skeleton,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Download as DownloadIcon,
  Print as PrintIcon,
} from '@mui/icons-material';

interface Column<T> {
  id: keyof T | 'actions';
  label: string;
  minWidth?: number;
  align?: 'left' | 'right' | 'center';
  format?: (value: any) => React.ReactNode;
  sortable?: boolean;
  filterable?: boolean;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  selectable?: boolean;
  onSelectionChange?: (selectedItems: T[]) => void;
  searchable?: boolean;
  searchFields?: (keyof T)[];
  exportable?: boolean;
  onExport?: (format: 'csv' | 'pdf') => void;
  printable?: boolean;
  onPrint?: () => void;
  emptyMessage?: string;
  rowsPerPageOptions?: number[];
  defaultRowsPerPage?: number;
  getRowId?: (row: T) => string | number;
}

export default function DataTable<T extends object>({
  columns,
  data,
  loading = false,
  selectable = false,
  onSelectionChange,
  searchable = true,
  searchFields,
  exportable = true,
  onExport,
  printable = true,
  onPrint,
  emptyMessage = 'لا توجد بيانات للعرض',
  rowsPerPageOptions = [10, 25, 50, 100],
  defaultRowsPerPage = 10,
  getRowId = (row: any) => row.id,
}: DataTableProps<T>) {
  const theme = useTheme();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(defaultRowsPerPage);
  const [searchQuery, setSearchQuery] = useState('');
  const [orderBy, setOrderBy] = useState<keyof T | ''>('');
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');
  const [selected, setSelected] = useState<T[]>([]);

  // تصفية البيانات حسب البحث
  const filteredData = useMemo(() => {
    if (!searchQuery || !searchFields) return data;

    return data.filter((row) =>
      searchFields.some((field) => {
        const value = row[field];
        if (typeof value === 'string' || typeof value === 'number') {
          return String(value)
            .toLowerCase()
            .includes(searchQuery.toLowerCase());
        }
        return false;
      })
    );
  }, [data, searchQuery, searchFields]);

  // ترتيب البيانات
  const sortedData = useMemo(() => {
    if (!orderBy) return filteredData;

    return [...filteredData].sort((a, b) => {
      const aValue = a[orderBy as keyof T];
      const bValue = b[orderBy as keyof T];

      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return order === 'asc'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }

      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return order === 'asc' ? aValue - bValue : bValue - aValue;
      }

      return 0;
    });
  }, [filteredData, orderBy, order]);

  // الصفحة الحالية من البيانات
  const paginatedData = useMemo(() => {
    const start = page * rowsPerPage;
    return sortedData.slice(start, start + rowsPerPage);
  }, [sortedData, page, rowsPerPage]);

  const handleSort = (columnId: keyof T) => {
    const isAsc = orderBy === columnId && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(columnId);
  };

  const handleSelectAll = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      setSelected(paginatedData);
      onSelectionChange?.(paginatedData);
    } else {
      setSelected([]);
      onSelectionChange?.([]);
    }
  };

  const handleSelect = (row: T) => {
    const selectedIndex = selected.findIndex((item) => getRowId(item) === getRowId(row));
    let newSelected: T[] = [];

    if (selectedIndex === -1) {
      newSelected = [...selected, row];
    } else {
      newSelected = selected.filter((_, index) => index !== selectedIndex);
    }

    setSelected(newSelected);
    onSelectionChange?.(newSelected);
  };

  const isSelected = (row: T) => selected.findIndex((item) => getRowId(item) === getRowId(row)) !== -1;

  return (
    <Paper
      sx={{
        width: '100%',
        overflow: 'hidden',
        boxShadow: theme.shadows[2],
        borderRadius: 2,
      }}
    >
      {/* شريط الأدوات */}
      <Box
        sx={{
          p: 2,
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          borderBottom: `1px solid ${theme.palette.divider}`,
        }}
      >
        {searchable && (
          <TextField
            size="small"
            placeholder="بحث..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon sx={{ color: 'text.secondary', mr: 1 }} />,
            }}
            sx={{ minWidth: 200 }}
          />
        )}

        <Box sx={{ flexGrow: 1 }} />

        {exportable && (
          <Tooltip title="تصدير">
            <IconButton onClick={() => onExport?.('csv')}>
              <DownloadIcon />
            </IconButton>
          </Tooltip>
        )}

        {printable && (
          <Tooltip title="طباعة">
            <IconButton onClick={onPrint}>
              <PrintIcon />
            </IconButton>
          </Tooltip>
        )}

        <Tooltip title="تصفية">
          <IconButton>
            <FilterIcon />
          </IconButton>
        </Tooltip>
      </Box>

      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {selectable && (
                <TableCell padding="checkbox">
                  <Checkbox
                    indeterminate={selected.length > 0 && selected.length < paginatedData.length}
                    checked={paginatedData.length > 0 && selected.length === paginatedData.length}
                    onChange={handleSelectAll}
                  />
                </TableCell>
              )}
              {columns.map((column) => (
                <TableCell
                  key={String(column.id)}
                  align={column.align}
                  style={{ minWidth: column.minWidth }}
                  sortDirection={orderBy === column.id ? order : false}
                >
                  {column.sortable ? (
                    <TableSortLabel
                      active={orderBy === column.id}
                      direction={orderBy === column.id ? order : 'asc'}
                      onClick={() => handleSort(column.id as keyof T)}
                    >
                      {column.label}
                    </TableSortLabel>
                  ) : (
                    column.label
                  )}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              Array.from({ length: rowsPerPage }).map((_, index) => (
                <TableRow key={index}>
                  {selectable && (
                    <TableCell padding="checkbox">
                      <Skeleton variant="rectangular" width={20} height={20} />
                    </TableCell>
                  )}
                  {columns.map((column) => (
                    <TableCell key={String(column.id)}>
                      <Skeleton variant="text" />
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : paginatedData.length > 0 ? (
              paginatedData.map((row) => {
                const isItemSelected = isSelected(row);
                return (
                  <TableRow
                    hover
                    key={getRowId(row)}
                    selected={isItemSelected}
                    sx={{
                      cursor: selectable ? 'pointer' : 'default',
                      '&.Mui-selected, &.Mui-selected:hover': {
                        backgroundColor: alpha(theme.palette.primary.main, 0.08),
                      },
                    }}
                    onClick={() => selectable && handleSelect(row)}
                  >
                    {selectable && (
                      <TableCell padding="checkbox">
                        <Checkbox checked={isItemSelected} />
                      </TableCell>
                    )}
                    {columns.map((column) => {
                      const value = row[column.id as keyof T];
                      return (
                        <TableCell key={String(column.id)} align={column.align}>
                          {column.format ? column.format(value) : value}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                );
              })
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length + (selectable ? 1 : 0)}
                  align="center"
                  sx={{ py: 8 }}
                >
                  <Typography color="text.secondary">{emptyMessage}</Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        component="div"
        count={sortedData.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={(_, newPage) => setPage(newPage)}
        onRowsPerPageChange={(e) => {
          setRowsPerPage(parseInt(e.target.value, 10));
          setPage(0);
        }}
        rowsPerPageOptions={rowsPerPageOptions}
        labelRowsPerPage="عدد الصفوف في الصفحة:"
        labelDisplayedRows={({ from, to, count }) =>
          `${from}-${to} من ${count !== -1 ? count : `أكثر من ${to}`}`
        }
      />
    </Paper>
  );
}

// Web Worker لمعالجة بيانات الجدول
self.onmessage = (event) => {
  const { data, sortConfig } = event.data;

  if (sortConfig) {
    const sortedData = [...data].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortConfig.direction === 'asc'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }

      return sortConfig.direction === 'asc'
        ? aValue - bValue
        : bValue - aValue;
    });

    self.postMessage(sortedData);
  } else {
    self.postMessage(data);
  }
};

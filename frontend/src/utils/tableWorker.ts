// Web Worker لمعالجة بيانات الجدول
export {};

const worker = self as unknown as Worker;

worker.onmessage = (event: MessageEvent) => {
  const { data, sortBy, sortDirection } = event.data;

  // Sort data
  const sortedData = data.sort((a: any, b: any) => {
    if (sortDirection === 'asc') {
      return a[sortBy] > b[sortBy] ? 1 : -1;
    }
    return a[sortBy] < b[sortBy] ? 1 : -1;
  });

  worker.postMessage(sortedData);
};

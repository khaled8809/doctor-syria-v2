export interface Analytics {
  predictions: {
    patientLoad: any[];
    resourceNeeds: any[];
    staffingRequirements: any[];
  };
  departmentPerformance: {
    efficiency: number;
    satisfaction: number;
    waitTimes: number;
  };
  resourceUtilization: {
    beds: number;
    equipment: number;
    staff: number;
  };
  financialMetrics: {
    revenue: number;
    expenses: number;
    profit: number;
  };
}

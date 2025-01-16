export interface Analytics {
  patientMetrics: {
    total: number;
    admitted: number;
    discharged: number;
    critical: number;
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
  predictions?: {
    patientLoad: any[];
    resourceNeeds: any[];
    staffingRequirements: any[];
  };
  nurseMetrics?: {
    taskCompletion: number;
    responseTime: number;
    patientSatisfaction: number;
  };
  doctorStats?: {
    patientsSeen: number;
    avgConsultationTime: number;
    successRate: number;
  };
}

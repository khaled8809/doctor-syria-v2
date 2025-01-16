export interface Analytics {
  patientMetrics: {
    total: number;
    admitted: number;
    discharged: number;
    critical: number;
    byDepartment: { [key: string]: number };
    byAge: {
      '0-18': number;
      '19-30': number;
      '31-50': number;
      '51-70': number;
      '70+': number;
    };
    byGender: {
      male: number;
      female: number;
      other: number;
    };
    averageStayDuration: number;
    readmissionRate: number;
  };
  departmentPerformance: {
    efficiency: number;
    satisfaction: number;
    waitTimes: number;
    staffUtilization: number;
    patientThroughput: number;
    bedTurnoverRate: number;
    departmentSpecificMetrics: {
      [department: string]: {
        specializedMetric1: number;
        specializedMetric2: number;
      };
    };
  };
  resourceUtilization: {
    beds: number;
    equipment: number;
    staff: number;
    byDepartment: {
      [department: string]: {
        beds: number;
        equipment: number;
        staff: number;
      };
    };
    utilizationTrends: {
      date: string;
      beds: number;
      equipment: number;
      staff: number;
    }[];
  };
  financialMetrics: {
    revenue: number;
    expenses: number;
    profit: number;
    byDepartment: {
      [department: string]: {
        revenue: number;
        expenses: number;
        profit: number;
      };
    };
    trends: {
      date: string;
      revenue: number;
      expenses: number;
      profit: number;
    }[];
    insuranceClaims: {
      submitted: number;
      approved: number;
      pending: number;
      rejected: number;
    };
  };
  predictions: {
    patientLoad: {
      date: string;
      predicted: number;
      actual?: number;
      byDepartment: { [key: string]: number };
    }[];
    resourceNeeds: {
      date: string;
      staff: number;
      beds: number;
      equipment: number;
      byDepartment: { [key: string]: number };
    }[];
    staffingRequirements: {
      date: string;
      doctors: number;
      nurses: number;
      specialists: number;
      byDepartment: { [key: string]: number };
    }[];
    emergencyPredictions: {
      date: string;
      likelihood: number;
      type: string;
      requiredResources: string[];
    }[];
  };
  nurseMetrics: {
    taskCompletion: number;
    responseTime: number;
    patientSatisfaction: number;
    workload: {
      current: number;
      optimal: number;
      overloaded: boolean;
    };
    shiftPerformance: {
      shift: 'morning' | 'afternoon' | 'night';
      efficiency: number;
      incidents: number;
    }[];
    specializations: {
      type: string;
      count: number;
      utilization: number;
    }[];
  };
  doctorStats: {
    patientsSeen: number;
    avgConsultationTime: number;
    successRate: number;
    specialtyPerformance: {
      specialty: string;
      patients: number;
      satisfaction: number;
      outcomes: {
        success: number;
        failure: number;
        followup: number;
      };
    }[];
    availability: {
      scheduled: number;
      actual: number;
      variance: number;
    };
    research: {
      publications: number;
      ongoing: number;
      collaborations: number;
    };
  };
  qualityMetrics: {
    patientSatisfaction: number;
    incidentReports: number;
    complianceRate: number;
    infectionRates: number;
    readmissionRates: number;
    mortalityRates: number;
    medicationErrors: number;
    waitingTimes: {
      emergency: number;
      outpatient: number;
      specialist: number;
    };
  };
  operationalMetrics: {
    bedOccupancy: number;
    averageLengthOfStay: number;
    emergencyResponseTime: number;
    operatingRoomUtilization: number;
    equipmentDowntime: number;
    suppliesInventory: {
      item: string;
      current: number;
      minimum: number;
      reorderPoint: number;
    }[];
  };
}

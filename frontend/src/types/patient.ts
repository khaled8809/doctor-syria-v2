export interface MedicalRecord {
  condition: string;
  diagnosedDate: string;
  notes: string;
}

export interface Visit {
  date: string;
  doctor: string;
  reason: string;
  notes: string;
}

export interface Patient {
  id: string;
  patientId: string;
  firstName: string;
  lastName: string;
  photoUrl?: string;
  status: string;
  age: number;
  gender: string;
  phone: string;
  address: string;
  medicalHistory: MedicalRecord[];
  visits: Visit[];
}

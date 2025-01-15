export interface MedicalRecord {
  id: string;
  date: string;
  condition: string;
  treatment: string;
  notes?: string;
}

export interface Visit {
  id: string;
  date: string;
  reason: string;
  diagnosis?: string;
  prescription?: string;
  notes?: string;
}

export interface Patient {
  id: string;
  firstName: string;
  lastName: string;
  patientId: string;
  fileNumber: string;
  doctorId: string;
  photoUrl?: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  phone: string;
  address: string;
  status: 'active' | 'inactive';
  medicalHistory: MedicalRecord[];
  visits: Visit[];
}

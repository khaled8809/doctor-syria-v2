import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DiagnosisSession from '../DiagnosisSession';
import { useAIService } from '../../../services/ai-service';
import { usePatientContext } from '../../../contexts/PatientContext';

// Mock the hooks
jest.mock('../../../services/ai-service');
jest.mock('../../../contexts/PatientContext');

const mockPatient = {
  id: 1,
  name: 'أحمد محمد',
};

const mockDiagnosisResults = [
  {
    disease: {
      name: 'التهاب الحلق',
      icd_code: 'J02.9',
      risk_level: 1,
    },
    confidence: 85,
    reasoning: {
      matching_symptoms: [
        { name: 'ألم في الحلق', importance: 3 },
        { name: 'صعوبة في البلع', importance: 2 },
      ],
      missing_symptoms: [
        { name: 'حمى', importance: 2 },
      ],
      confidence_explanation: 'ثقة عالية بناءً على تطابق الأعراض الرئيسية',
    },
    recommendations: 'يُنصح بالراحة وشرب السوائل الدافئة',
  },
];

describe('DiagnosisSession Component', () => {
  beforeEach(() => {
    // Reset all mocks
    jest.clearAllMocks();

    // Mock the hooks implementation
    (usePatientContext as jest.Mock).mockReturnValue({
      currentPatient: mockPatient,
    });

    (useAIService as jest.Mock).mockReturnValue({
      startDiagnosis: jest.fn().mockResolvedValue(mockDiagnosisResults),
      getDiagnosisResults: jest.fn().mockResolvedValue(mockDiagnosisResults),
    });
  });

  it('renders correctly with patient information', () => {
    render(<DiagnosisSession />);
    
    expect(screen.getByText('التشخيص الذكي')).toBeInTheDocument();
    expect(screen.getByText(`المريض: ${mockPatient.name}`)).toBeInTheDocument();
    expect(screen.getByText('اختيار الأعراض')).toBeInTheDocument();
  });

  it('shows error when trying to proceed without symptoms', async () => {
    render(<DiagnosisSession />);
    
    const nextButton = screen.getByText('التالي');
    fireEvent.click(nextButton);
    
    expect(await screen.findByText('الرجاء اختيار عرض واحد على الأقل')).toBeInTheDocument();
  });

  it('proceeds through diagnosis steps correctly', async () => {
    const { startDiagnosis } = useAIService();
    render(<DiagnosisSession />);

    // Add a symptom (this will be simulated since SymptomSelector is mocked)
    const mockSymptom = {
      symptom_id: 1,
      name: 'ألم في الحلق',
      severity: 2,
    };

    // Simulate adding a symptom
    fireEvent.click(screen.getByText('التالي'));
    await waitFor(() => {
      expect(startDiagnosis).toHaveBeenCalledWith({
        patientId: mockPatient.id,
        symptoms: [mockSymptom],
      });
    });
  });

  it('displays loading state during diagnosis', async () => {
    render(<DiagnosisSession />);
    
    // Move to diagnosis step
    const nextButton = screen.getByText('التالي');
    fireEvent.click(nextButton);
    
    expect(screen.getByText('جاري تحليل الأعراض...')).toBeInTheDocument();
  });

  it('handles API errors gracefully', async () => {
    // Mock API error
    (useAIService as jest.Mock).mockReturnValue({
      startDiagnosis: jest.fn().mockRejectedValue(new Error('API Error')),
    });

    render(<DiagnosisSession />);
    
    const nextButton = screen.getByText('التالي');
    fireEvent.click(nextButton);
    
    expect(await screen.findByText('حدث خطأ أثناء التشخيص. الرجاء المحاولة مرة أخرى.')).toBeInTheDocument();
  });

  it('allows navigation between steps', async () => {
    render(<DiagnosisSession />);
    
    // Initially at step 1
    expect(screen.getByText('اختيار الأعراض')).toBeInTheDocument();
    
    // Move forward
    const nextButton = screen.getByText('التالي');
    fireEvent.click(nextButton);
    
    // Try to go back
    const backButton = screen.getByText('رجوع');
    fireEvent.click(backButton);
    
    // Should be back at step 1
    expect(screen.getByText('اختيار الأعراض')).toBeInTheDocument();
  });
});

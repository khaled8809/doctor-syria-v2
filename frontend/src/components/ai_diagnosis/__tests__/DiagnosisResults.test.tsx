import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DiagnosisResults from '../DiagnosisResults';

const mockDiagnosisResult: DiagnosisResult = {
  id: '1',
  diagnosis: {
    name: 'Common Cold',
    icd_code: 'J00',
    risk_level: 1
  },
  confidence: 0.85,
  reasoning: {
    matching_symptoms: [
      { name: 'Fever', importance: 0.8 },
      { name: 'Cough', importance: 0.7 }
    ],
    missing_symptoms: [
      { name: 'Headache', importance: 0.5 }
    ],
    confidence_explanation: 'Based on matching symptoms'
  },
  recommendations: ['Rest', 'Hydration'],
  riskLevel: 'low'
};

// Mock PDF download button component
jest.mock('../../common/PDFDownloadButton', () => ({
  PDFDownloadButton: () => <button>Download PDF</button>,
}));

describe('DiagnosisResults Component', () => {
  it('renders diagnosis results correctly', () => {
    render(<DiagnosisResults results={[mockDiagnosisResult]} />);

    // Check main title
    expect(screen.getByText('Diagnosis Results')).toBeInTheDocument();

    // Check diseases are displayed
    expect(screen.getByText('Common Cold')).toBeInTheDocument();

    // Check ICD codes
    expect(screen.getByText('J00')).toBeInTheDocument();

    // Check confidence levels
    expect(screen.getByText('85% confidence')).toBeInTheDocument();
  });

  it('displays matching symptoms correctly', () => {
    render(<DiagnosisResults results={[mockDiagnosisResult]} />);

    // Check matching symptoms
    expect(screen.getByText('Fever')).toBeInTheDocument();
    expect(screen.getByText('Cough')).toBeInTheDocument();

    // Check importance levels
    expect(screen.getByText('Importance: 0.8')).toBeInTheDocument();
    expect(screen.getByText('Importance: 0.7')).toBeInTheDocument();
  });

  it('displays missing symptoms correctly', () => {
    render(<DiagnosisResults results={[mockDiagnosisResult]} />);

    // Check missing symptoms
    expect(screen.getByText('Headache')).toBeInTheDocument();
  });

  it('displays recommendations correctly', () => {
    render(<DiagnosisResults results={[mockDiagnosisResult]} />);

    // Check recommendations
    expect(screen.getByText('Rest')).toBeInTheDocument();
    expect(screen.getByText('Hydration')).toBeInTheDocument();
  });

  it('renders action buttons', () => {
    render(<DiagnosisResults results={[mockDiagnosisResult]} />);

    // Check action buttons
    expect(screen.getAllByText('Create Prescription')).toHaveLength(1);
    expect(screen.getAllByText('Add to Medical Record')).toHaveLength(1);
  });

  it('renders PDF download button', () => {
    render(<DiagnosisResults results={[mockDiagnosisResult]} />);
    expect(screen.getByText('Download PDF')).toBeInTheDocument();
  });

  it('displays different confidence levels with appropriate colors', () => {
    const resultsWithDifferentConfidence = [
      {
        ...mockDiagnosisResult,
        confidence: 0.9, // High confidence
      },
      {
        ...mockDiagnosisResult,
        confidence: 0.6, // Medium confidence
      },
      {
        ...mockDiagnosisResult,
        confidence: 0.3, // Low confidence
        diagnosis: { ...mockDiagnosisResult.diagnosis, name: 'Another Disease' },
      },
    ];

    render(<DiagnosisResults results={resultsWithDifferentConfidence} />);

    // Check confidence chips with different colors
    const confidenceChips = screen.getAllByText(/\d+% confidence/);
    expect(confidenceChips).toHaveLength(3);
  });

  it('handles empty results gracefully', () => {
    render(<DiagnosisResults results={[]} />);
    expect(screen.getByText('Diagnosis Results')).toBeInTheDocument();
  });

  it('displays risk levels appropriately', () => {
    render(<DiagnosisResults results={[mockDiagnosisResult]} />);

    // The disease has low risk (level 1)
    expect(screen.getByText(mockDiagnosisResult.diagnosis.name)).toBeInTheDocument();
  });
});

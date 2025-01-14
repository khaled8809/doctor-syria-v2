import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DiagnosisResults from '../DiagnosisResults';

const mockResults = [
  {
    disease: {
      name: 'التهاب الحلق',
      icd_code: 'J02.9',
      risk_level: 2,
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
  {
    disease: {
      name: 'التهاب اللوزتين',
      icd_code: 'J03.9',
      risk_level: 3,
    },
    confidence: 65,
    reasoning: {
      matching_symptoms: [
        { name: 'ألم في الحلق', importance: 3 },
      ],
      missing_symptoms: [
        { name: 'تورم اللوزتين', importance: 3 },
        { name: 'حمى مرتفعة', importance: 2 },
      ],
      confidence_explanation: 'ثقة متوسطة مع وجود بعض الأعراض المطابقة',
    },
    recommendations: 'يُنصح بمراجعة الطبيب في أقرب وقت ممكن',
  },
];

// Mock PDF download button component
jest.mock('../../common/PDFDownloadButton', () => ({
  PDFDownloadButton: () => <button>تحميل PDF</button>,
}));

describe('DiagnosisResults Component', () => {
  it('renders diagnosis results correctly', () => {
    render(<DiagnosisResults results={mockResults} />);

    // Check main title
    expect(screen.getByText('نتائج التشخيص')).toBeInTheDocument();

    // Check diseases are displayed
    expect(screen.getByText('التهاب الحلق')).toBeInTheDocument();
    expect(screen.getByText('التهاب اللوزتين')).toBeInTheDocument();

    // Check ICD codes
    expect(screen.getByText('J02.9')).toBeInTheDocument();
    expect(screen.getByText('J03.9')).toBeInTheDocument();

    // Check confidence levels
    expect(screen.getByText('85% ثقة')).toBeInTheDocument();
    expect(screen.getByText('65% ثقة')).toBeInTheDocument();
  });

  it('displays matching symptoms correctly', () => {
    render(<DiagnosisResults results={mockResults} />);

    // Check matching symptoms
    expect(screen.getByText('ألم في الحلق')).toBeInTheDocument();
    expect(screen.getByText('صعوبة في البلع')).toBeInTheDocument();

    // Check importance levels
    expect(screen.getByText('درجة الأهمية: 3')).toBeInTheDocument();
    expect(screen.getByText('درجة الأهمية: 2')).toBeInTheDocument();
  });

  it('displays missing symptoms correctly', () => {
    render(<DiagnosisResults results={mockResults} />);

    // Check missing symptoms
    expect(screen.getByText('حمى')).toBeInTheDocument();
    expect(screen.getByText('تورم اللوزتين')).toBeInTheDocument();
    expect(screen.getByText('حمى مرتفعة')).toBeInTheDocument();
  });

  it('displays recommendations correctly', () => {
    render(<DiagnosisResults results={mockResults} />);

    // Check recommendations
    expect(screen.getByText('يُنصح بالراحة وشرب السوائل الدافئة')).toBeInTheDocument();
    expect(screen.getByText('يُنصح بمراجعة الطبيب في أقرب وقت ممكن')).toBeInTheDocument();
  });

  it('renders action buttons', () => {
    render(<DiagnosisResults results={mockResults} />);

    // Check action buttons
    expect(screen.getAllByText('إنشاء وصفة طبية')).toHaveLength(2);
    expect(screen.getAllByText('إضافة إلى السجل الطبي')).toHaveLength(2);
  });

  it('renders PDF download button', () => {
    render(<DiagnosisResults results={mockResults} />);
    expect(screen.getByText('تحميل PDF')).toBeInTheDocument();
  });

  it('displays different confidence levels with appropriate colors', () => {
    const resultsWithDifferentConfidence = [
      {
        ...mockResults[0],
        confidence: 90, // High confidence
      },
      {
        ...mockResults[1],
        confidence: 60, // Medium confidence
      },
      {
        ...mockResults[1],
        confidence: 30, // Low confidence
        disease: { ...mockResults[1].disease, name: 'مرض آخر' },
      },
    ];

    render(<DiagnosisResults results={resultsWithDifferentConfidence} />);

    // Check confidence chips with different colors
    const confidenceChips = screen.getAllByText(/\d+% ثقة/);
    expect(confidenceChips).toHaveLength(3);
  });

  it('handles empty results gracefully', () => {
    render(<DiagnosisResults results={[]} />);
    expect(screen.getByText('نتائج التشخيص')).toBeInTheDocument();
  });

  it('displays risk levels appropriately', () => {
    render(<DiagnosisResults results={mockResults} />);

    // The second disease has high risk (level 3)
    const highRiskDisease = mockResults[1];
    expect(screen.getByText(highRiskDisease.disease.name)).toBeInTheDocument();
  });
});

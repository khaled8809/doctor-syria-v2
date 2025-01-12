import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SymptomSelector from '../SymptomSelector';
import { useAIService } from '../../../services/ai-service';

// Mock the AI service hook
jest.mock('../../../services/ai-service');

const mockSymptoms = [
  {
    id: 1,
    name: 'ألم في الحلق',
    description: 'ألم وحرقة في الحلق',
  },
  {
    id: 2,
    name: 'صداع',
    description: 'ألم في الرأس',
  },
  {
    id: 3,
    name: 'حمى',
    description: 'ارتفاع في درجة الحرارة',
  },
];

describe('SymptomSelector Component', () => {
  const mockOnSymptomSelect = jest.fn();
  const mockOnSymptomRemove = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock the AI service implementation
    (useAIService as jest.Mock).mockReturnValue({
      getSymptoms: jest.fn().mockResolvedValue(mockSymptoms),
    });
  });

  it('renders correctly with initial state', async () => {
    render(
      <SymptomSelector
        selectedSymptoms={[]}
        onSymptomSelect={mockOnSymptomSelect}
        onSymptomRemove={mockOnSymptomRemove}
      />
    );

    expect(screen.getByText('إضافة الأعراض')).toBeInTheDocument();
    expect(screen.getByText('شدة العرض')).toBeInTheDocument();
    expect(screen.getByText('الأعراض المختارة')).toBeInTheDocument();
    expect(screen.getByText('لم يتم اختيار أي أعراض بعد')).toBeInTheDocument();
  });

  it('loads and displays symptoms from API', async () => {
    render(
      <SymptomSelector
        selectedSymptoms={[]}
        onSymptomSelect={mockOnSymptomSelect}
        onSymptomRemove={mockOnSymptomRemove}
      />
    );

    // Wait for symptoms to load
    await waitFor(() => {
      const autocomplete = screen.getByRole('combobox');
      expect(autocomplete).toBeInTheDocument();
    });
  });

  it('allows selecting a symptom with severity and notes', async () => {
    render(
      <SymptomSelector
        selectedSymptoms={[]}
        onSymptomSelect={mockOnSymptomSelect}
        onSymptomRemove={mockOnSymptomRemove}
      />
    );

    // Wait for symptoms to load
    await waitFor(() => {
      const autocomplete = screen.getByRole('combobox');
      expect(autocomplete).toBeInTheDocument();
    });

    // Select a symptom
    const autocomplete = screen.getByRole('combobox');
    fireEvent.change(autocomplete, { target: { value: 'ألم' } });
    
    // Select severity
    const severityRating = screen.getByRole('radio', { name: /3 Stars/i });
    fireEvent.click(severityRating);

    // Add notes
    const notesInput = screen.getByLabelText('ملاحظات إضافية');
    fireEvent.change(notesInput, { target: { value: 'ألم شديد في المساء' } });
  });

  it('displays selected symptoms correctly', () => {
    const selectedSymptoms = [
      {
        symptom_id: 1,
        name: 'ألم في الحلق',
        severity: 2,
        notes: 'ألم متوسط',
      },
    ];

    render(
      <SymptomSelector
        selectedSymptoms={selectedSymptoms}
        onSymptomSelect={mockOnSymptomSelect}
        onSymptomRemove={mockOnSymptomRemove}
      />
    );

    expect(screen.getByText('ألم في الحلق')).toBeInTheDocument();
    expect(screen.getByText('ألم متوسط')).toBeInTheDocument();
  });

  it('allows removing selected symptoms', () => {
    const selectedSymptoms = [
      {
        symptom_id: 1,
        name: 'ألم في الحلق',
        severity: 2,
        notes: 'ألم متوسط',
      },
    ];

    render(
      <SymptomSelector
        selectedSymptoms={selectedSymptoms}
        onSymptomSelect={mockOnSymptomSelect}
        onSymptomRemove={mockOnSymptomRemove}
      />
    );

    // Click delete button
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);

    expect(mockOnSymptomRemove).toHaveBeenCalledWith(1);
  });

  it('handles API errors gracefully', async () => {
    // Mock API error
    (useAIService as jest.Mock).mockReturnValue({
      getSymptoms: jest.fn().mockRejectedValue(new Error('API Error')),
    });

    render(
      <SymptomSelector
        selectedSymptoms={[]}
        onSymptomSelect={mockOnSymptomSelect}
        onSymptomRemove={mockOnSymptomRemove}
      />
    );

    // Wait for error handling
    await waitFor(() => {
      expect(console.error).toHaveBeenCalled();
    });
  });

  it('validates symptom selection before adding', async () => {
    render(
      <SymptomSelector
        selectedSymptoms={[]}
        onSymptomSelect={mockOnSymptomSelect}
        onSymptomRemove={mockOnSymptomRemove}
      />
    );

    // Try to add without selecting a symptom
    const addButton = screen.getByRole('button', { name: /إضافة/i });
    fireEvent.click(addButton);

    expect(mockOnSymptomSelect).not.toHaveBeenCalled();
  });
});

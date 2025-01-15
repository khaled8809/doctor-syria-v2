import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SymptomSelector from '../SymptomSelector';
import { Symptom } from '../../../types/diagnosis';

const mockSymptoms: Symptom[] = [
  { symptom_id: 1, name: 'Fever', severity: 3 },
  { symptom_id: 2, name: 'Cough', severity: 2 },
  { symptom_id: 3, name: 'Headache', severity: 1 }
];

describe('SymptomSelector', () => {
  const mockOnSelect = jest.fn();
  const mockOnRemove = jest.fn();

  beforeEach(() => {
    render(
      <SymptomSelector
        selectedSymptoms={mockSymptoms}
        onSymptomSelect={mockOnSelect}
        onSymptomRemove={mockOnRemove}
      />
    );
  });

  it('renders symptom input field', () => {
    expect(screen.getByPlaceholderText('Search symptoms...')).toBeInTheDocument();
  });

  it('displays selected symptoms', () => {
    mockSymptoms.forEach(symptom => {
      expect(screen.getByText(symptom.name)).toBeInTheDocument();
    });
  });

  it('allows removing symptoms', async () => {
    const removeButtons = screen.getAllByRole('button', { name: /remove/i });
    await userEvent.click(removeButtons[0]);
    expect(mockOnRemove).toHaveBeenCalledWith(mockSymptoms[0].symptom_id);
  });
});

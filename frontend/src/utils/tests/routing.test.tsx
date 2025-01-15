import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../../App';

describe('Routing', () => {
  it('renders main app with router', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    // Add assertions here
  });
});

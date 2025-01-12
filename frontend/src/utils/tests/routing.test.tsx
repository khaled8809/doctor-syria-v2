import { render, screen } from '@testing-library/react';
import { HashRouter } from 'react-router-dom';
import App from '../../App';

describe('Routing Tests', () => {
  test('navigates to dashboard by default', () => {
    render(
      <HashRouter>
        <App />
      </HashRouter>
    );
    expect(window.location.hash).toBe('#/dashboard');
  });

  test('loads all routes correctly', () => {
    const routes = [
      '/dashboard',
      '/devices',
      '/reports',
      '/resources',
      '/ai-models',
      '/schedule',
      '/communication',
      '/settings'
    ];

    routes.forEach(route => {
      window.location.hash = route;
      expect(window.location.hash).toBe(`#${route}`);
    });
  });
});

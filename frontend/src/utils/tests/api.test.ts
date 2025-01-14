import axios from 'axios';

describe('API Connection Tests', () => {
  const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';

  test('API endpoint is reachable', async () => {
    try {
      const response = await axios.get(`${API_URL}/health`);
      expect(response.status).toBe(200);
    } catch (error) {
      console.error('API health check failed:', error);
      throw error;
    }
  });

  test('API authentication works', async () => {
    try {
      const response = await axios.post(`${API_URL}/auth/test`, {
        test: true
      });
      expect(response.status).toBe(200);
    } catch (error) {
      console.error('API auth test failed:', error);
      throw error;
    }
  });
});

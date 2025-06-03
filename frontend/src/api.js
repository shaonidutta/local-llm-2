/**
 * API client for Local AI Writer backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes timeout for generation
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🔄 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

/**
 * Generate text using the local AI model
 * @param {string} prompt - The text prompt
 * @param {number} temperature - Sampling temperature (0.0 to 1.0)
 * @param {number} maxNewTokens - Maximum new tokens to generate
 * @returns {Promise<Object>} Generation response
 */
export const generateText = async (prompt, temperature = 0.7, maxNewTokens = 200) => {
  try {
    const response = await apiClient.post('/generate', {
      prompt,
      temperature,
      max_new_tokens: maxNewTokens,
    });
    
    return response.data;
  } catch (error) {
    console.error('Generation failed:', error);
    
    if (error.response) {
      // Server responded with error status
      throw new Error(`Server error: ${error.response.data?.detail || error.response.statusText}`);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('No response from server. Please check if the backend is running.');
    } else {
      // Something else happened
      throw new Error(`Request failed: ${error.message}`);
    }
  }
};

/**
 * Check API health status
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw new Error('Backend is not responding');
  }
};

/**
 * Get recent logs from the backend
 * @param {number} lines - Number of recent lines to fetch
 * @returns {Promise<Object>} Logs data
 */
export const getLogs = async (lines = 50) => {
  try {
    const response = await apiClient.get(`/logs?lines=${lines}`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch logs:', error);
    throw new Error('Could not fetch logs');
  }
};

/**
 * Get API root information
 * @returns {Promise<Object>} API info
 */
export const getApiInfo = async () => {
  try {
    const response = await apiClient.get('/');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch API info:', error);
    throw new Error('Could not fetch API information');
  }
};

export default apiClient;

/**
 * API Service
 * Handles all HTTP requests to the backend API
 */

import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API methods
export const apiService = {
  // Generate synthetic logs
  generateLogs: async () => {
    const response = await api.post('/generate-logs');
    return response.data;
  },

  // Train ML model
  trainModel: async () => {
    const response = await api.post('/train-model');
    return response.data;
  },

  // Analyze logs
  analyzeLogs: async () => {
    const response = await api.post('/analyze-logs');
    return response.data;
  },

  // Get alerts with optional risk level filter
  getAlerts: async (riskLevel = null, limit = 100) => {
    const params = { limit };
    if (riskLevel) {
      params.risk_level = riskLevel;
    }
    const response = await api.get('/alerts', { params });
    return response.data;
  },

  // Get dashboard statistics
  getDashboardStats: async () => {
    const response = await api.get('/dashboard-stats');
    return response.data;
  },

  // Get risk trend
  getRiskTrend: async (hours = 24) => {
    const response = await api.get('/risk-trend', { params: { hours } });
    return response.data;
  },

  // Simulate attack
  simulateAttack: async () => {
    const response = await api.post('/simulate-attack');
    return response.data;
  },

  // Reset database
  resetDatabase: async () => {
    const response = await api.delete('/reset-database');
    return response.data;
  },
};

export default api;

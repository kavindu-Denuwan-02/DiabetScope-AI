/**
 * api.js
 * ──────
 * Centralized API service for backend communication.
 * 
 * WHY centralize API calls?
 *   • Single source of truth for backend URL
 *   • Consistent error handling
 *   • Easy to switch backends (dev → production)
 *   • Interview gold: shows clean architecture
 */

import axios from 'axios';

/**
 * ⚠️ IMPORTANT: Change this to your backend URL
 * 
 * Development (local machine):
 *   - If testing on physical device: 'http://YOUR_COMPUTER_IP:8000'
 *   - If testing on emulator: 'http://10.0.2.2:8000' (Android) or 'http://localhost:8000' (iOS)
 * 
 * Production (deployed backend):
 *   - 'https://your-backend.herokuapp.com' or your cloud URL
 */
const BASE_URL = 'http://192.168.1.100:8000'; // ← CHANGE THIS

/**
 * Create axios instance with default config.
 */
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000, // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Predict diabetes status (binary classification).
 * 
 * @param {object} data - Patient data
 * @param {number} data.pregnancies - Number of pregnancies
 * @param {number} data.glucose - Plasma glucose (mg/dL)
 * @param {number} data.blood_pressure - Diastolic BP (mm Hg)
 * @param {number} data.skin_thickness - Triceps skin fold (mm)
 * @param {number} data.insulin - 2-Hour serum insulin (μU/mL)
 * @param {number} data.bmi - Body Mass Index (kg/m²)
 * @param {number} data.diabetes_pedigree - Genetic score
 * @param {number} data.age - Age in years
 * 
 * @returns {Promise<object>} { prediction: string, probability: number }
 * 
 * @throws {Error} If API call fails
 */
export const predictDiabetes = async (data) => {
  try {
    const response = await api.post('/predict/diabetes', data);
    return response.data;
  } catch (error) {
    console.error('Diabetes prediction error:', error.response?.data || error.message);
    
    // Rethrow with user-friendly message
    if (error.response) {
      // Backend returned an error response
      throw new Error(
        error.response.data?.detail || 
        'Server error. Please try again.'
      );
    } else if (error.request) {
      // Request made but no response (network issue)
      throw new Error(
        'Cannot connect to server. Check your internet connection.'
      );
    } else {
      // Something else went wrong
      throw new Error('An unexpected error occurred.');
    }
  }
};

/**
 * Predict glucose level (regression).
 * 
 * @param {object} data - Patient data (WITHOUT glucose field)
 * @param {number} data.pregnancies
 * @param {number} data.blood_pressure
 * @param {number} data.skin_thickness
 * @param {number} data.insulin
 * @param {number} data.bmi
 * @param {number} data.diabetes_pedigree
 * @param {number} data.age
 * 
 * @returns {Promise<object>} { predicted_glucose: number }
 * 
 * @throws {Error} If API call fails
 */
export const predictGlucose = async (data) => {
  try {
    const response = await api.post('/predict/glucose', data);
    return response.data;
  } catch (error) {
    console.error('Glucose prediction error:', error.response?.data || error.message);
    
    if (error.response) {
      throw new Error(
        error.response.data?.detail || 
        'Server error. Please try again.'
      );
    } else if (error.request) {
      throw new Error(
        'Cannot connect to server. Check your internet connection.'
      );
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};

/**
 * Health check — verify backend is running.
 * 
 * @returns {Promise<boolean>} true if backend is healthy
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data.status === 'healthy';
  } catch (error) {
    console.error('Health check failed:', error.message);
    return false;
  }
};

export default {
  predictDiabetes,
  predictGlucose,
  checkHealth,
};

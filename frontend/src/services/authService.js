/**
 * Authentication service for API calls
 */

import { apiFetch, getApiUrl } from './apiClient';

/**
 * Sign up a new user
 * @param {Object} userData - User signup data
 * @returns {Promise<Object>} User data with token
 */
export const signup = async (userData) => {
  const response = await apiFetch(getApiUrl('/api/v1/auth/signup'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Signup failed');
  }

  return response.json();
};

/**
 * Login a user
 * @param {Object} credentials - User login credentials
 * @returns {Promise<Object>} User data with token
 */
export const login = async (credentials) => {
  const response = await apiFetch(getApiUrl('/api/v1/auth/login'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  return response.json();
};

/**
 * Get current user information
 * @param {string} token - JWT token
 * @returns {Promise<Object>} Current user data
 */
export const getCurrentUser = async (token) => {
  const response = await apiFetch(getApiUrl('/api/v1/auth/me'), {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get user info');
  }

  return response.json();
};

/**
 * Logout user
 * @param {string} token - JWT token
 * @returns {Promise<Object>} Logout response
 */
export const logout = async (token) => {
  const response = await apiFetch(getApiUrl('/api/v1/auth/logout'), {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Logout failed');
  }

  return response.json();
};

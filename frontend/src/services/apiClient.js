/**
 * API Client with global error handling and token expiration detection
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Callback for handling token expiration (set by AuthContext)
let onTokenExpiredCallback = null;

/**
 * Register callback to be called when token expires
 * @param {Function} callback - Function to call on token expiration
 */
export const setTokenExpiredCallback = (callback) => {
  onTokenExpiredCallback = callback;
};

/**
 * Enhanced fetch wrapper that handles token expiration
 * @param {string} url - API endpoint URL
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>} Fetch response
 */
export const apiFetch = async (url, options = {}) => {
  const response = await fetch(url, options);

  // Check if token expired (401 Unauthorized)
  if (response.status === 401 && onTokenExpiredCallback) {
    // Call the callback to handle logout
    onTokenExpiredCallback();
    
    // Throw error to prevent further processing
    throw new Error('Session expired. Please log in again.');
  }

  return response;
};

/**
 * Build full API URL
 * @param {string} path - API path
 * @returns {string} Full API URL
 */
export const getApiUrl = (path) => {
  return `${API_BASE_URL}${path}`;
};

export default apiFetch;

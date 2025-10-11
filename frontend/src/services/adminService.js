/**
 * Admin service for API calls
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const getAuthHeaders = (token) => ({
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json',
});

// User Management
export const getAllUsers = async (token, role = null) => {
  let url = `${API_BASE_URL}/api/v1/admin/users`;
  
  if (role) {
    url += `?role=${role}`;
  }

  const response = await fetch(url, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get users');
  }

  return response.json();
};

export const getUser = async (token, userId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/users/${userId}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get user');
  }

  return response.json();
};

export const updateUser = async (token, userId, userData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/users/${userId}`, {
    method: 'PUT',
    headers: getAuthHeaders(token),
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update user');
  }

  return response.json();
};

export const deleteUser = async (token, userId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/users/${userId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete user');
  }
};

// Platform Statistics
export const getPlatformStats = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/stats`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get platform stats');
  }

  return response.json();
};

// Usage Reports
export const generateUsageReport = async (token, days = 30) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/reports/usage?days=${days}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to generate usage report');
  }

  return response.json();
};

// Chart Data
export const getUserGrowthChart = async (token, days = 90) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/charts/user-growth?days=${days}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get user growth chart');
  }

  return response.json();
};

export const getPlatformUsageChart = async (token, days = 30) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/charts/platform-usage?days=${days}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get platform usage chart');
  }

  return response.json();
};

export const getCoachPerformanceChart = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/charts/coach-performance`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get coach performance chart');
  }

  return response.json();
};

export const getSystemHealthChart = async (token, days = 7) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/charts/system-health?days=${days}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get system health chart');
  }

  return response.json();
};

// Feedback Management
export const getAllFeedback = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/feedback/`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get feedback');
  }

  return response.json();
};

export const updateFeedbackStatus = async (token, feedbackId, status) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/feedback/${feedbackId}`, {
    method: 'PUT',
    headers: getAuthHeaders(token),
    body: JSON.stringify({ status }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update feedback status');
  }

  return response.json();
};

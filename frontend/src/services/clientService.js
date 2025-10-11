/**
 * Client service for API calls
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const getAuthHeaders = (token) => ({
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json',
});

// Workout Logs
export const createWorkoutLog = async (token, logData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/workout-logs`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify(logData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create workout log');
  }

  return response.json();
};

export const getWorkoutLogs = async (token, startDate = null, endDate = null) => {
  let url = `${API_BASE_URL}/api/v1/client/workout-logs`;
  const params = new URLSearchParams();
  
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  
  if (params.toString()) url += `?${params.toString()}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get workout logs');
  }

  return response.json();
};

export const updateWorkoutLog = async (token, logId, logData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/workout-logs/${logId}`, {
    method: 'PUT',
    headers: getAuthHeaders(token),
    body: JSON.stringify(logData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update workout log');
  }

  return response.json();
};

export const deleteWorkoutLog = async (token, logId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/workout-logs/${logId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete workout log');
  }
};

// Diet Logs
export const createDietLog = async (token, logData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/diet-logs`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify(logData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create diet log');
  }

  return response.json();
};

export const getDietLogs = async (token, startDate = null, endDate = null) => {
  let url = `${API_BASE_URL}/api/v1/client/diet-logs`;
  const params = new URLSearchParams();
  
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  
  if (params.toString()) url += `?${params.toString()}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get diet logs');
  }

  return response.json();
};

export const updateDietLog = async (token, logId, logData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/diet-logs/${logId}`, {
    method: 'PUT',
    headers: getAuthHeaders(token),
    body: JSON.stringify(logData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update diet log');
  }

  return response.json();
};

export const deleteDietLog = async (token, logId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/diet-logs/${logId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete diet log');
  }
};

// Plans
export const getWorkoutPlans = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/workout-plans`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get workout plans');
  }

  return response.json();
};

export const getDietPlans = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/diet-plans`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get diet plans');
  }

  return response.json();
};

// Progress
export const getProgress = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/progress`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get progress');
  }

  return response.json();
};

// Profile
export const updateProfile = async (token, profileData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/profile`, {
    method: 'PUT',
    headers: getAuthHeaders(token),
    body: JSON.stringify(profileData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update profile');
  }

  return response.json();
};

// Chart Data
export const getWorkoutFrequencyChart = async (token, days = 30) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/charts/workout-frequency?days=${days}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get workout frequency chart');
  }

  return response.json();
};

export const getDietAdherenceChart = async (token, days = 30) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/client/charts/diet-adherence?days=${days}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get diet adherence chart');
  }

  return response.json();
};

export const getWorkoutVolumeChart = async (token, days = 90, exercise = null) => {
  let url = `${API_BASE_URL}/api/v1/client/charts/workout-volume?days=${days}`;
  if (exercise) url += `&exercise=${encodeURIComponent(exercise)}`;
  
  const response = await fetch(url, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get workout volume chart');
  }

  return response.json();
};

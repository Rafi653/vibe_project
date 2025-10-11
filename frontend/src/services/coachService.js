/**
 * Coach service for API calls
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const getAuthHeaders = (token) => ({
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json',
});

// Client Management
export const getClients = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/clients`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get clients');
  }

  return response.json();
};

export const getClient = async (token, clientId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/clients/${clientId}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get client');
  }

  return response.json();
};

// View Client Logs
export const getClientWorkoutLogs = async (token, clientId, startDate = null, endDate = null) => {
  let url = `${API_BASE_URL}/api/v1/coach/clients/${clientId}/workout-logs`;
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
    throw new Error(error.detail || 'Failed to get client workout logs');
  }

  return response.json();
};

export const getClientDietLogs = async (token, clientId, startDate = null, endDate = null) => {
  let url = `${API_BASE_URL}/api/v1/coach/clients/${clientId}/diet-logs`;
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
    throw new Error(error.detail || 'Failed to get client diet logs');
  }

  return response.json();
};

export const getClientProgress = async (token, clientId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/clients/${clientId}/progress`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get client progress');
  }

  return response.json();
};

// Workout Plan Management
export const createWorkoutPlan = async (token, planData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/workout-plans`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify(planData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create workout plan');
  }

  return response.json();
};

export const getWorkoutPlans = async (token, clientId = null) => {
  let url = `${API_BASE_URL}/api/v1/coach/workout-plans`;
  
  if (clientId) {
    url += `?client_id=${clientId}`;
  }

  const response = await fetch(url, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get workout plans');
  }

  return response.json();
};

export const updateWorkoutPlan = async (token, planId, planData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/workout-plans/${planId}`, {
    method: 'PUT',
    headers: getAuthHeaders(token),
    body: JSON.stringify(planData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update workout plan');
  }

  return response.json();
};

export const deleteWorkoutPlan = async (token, planId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/workout-plans/${planId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete workout plan');
  }
};

// Diet Plan Management
export const createDietPlan = async (token, planData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/diet-plans`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify(planData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create diet plan');
  }

  return response.json();
};

export const getDietPlans = async (token, clientId = null) => {
  let url = `${API_BASE_URL}/api/v1/coach/diet-plans`;
  
  if (clientId) {
    url += `?client_id=${clientId}`;
  }

  const response = await fetch(url, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get diet plans');
  }

  return response.json();
};

export const updateDietPlan = async (token, planId, planData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/diet-plans/${planId}`, {
    method: 'PUT',
    headers: getAuthHeaders(token),
    body: JSON.stringify(planData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update diet plan');
  }

  return response.json();
};

export const deleteDietPlan = async (token, planId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/diet-plans/${planId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete diet plan');
  }
};

// Chart Data
export const getClientOverviewChart = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/charts/client-overview`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get client overview chart');
  }

  return response.json();
};

export const getEngagementChart = async (token, days = 30) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/charts/engagement?days=${days}`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get engagement chart');
  }

  return response.json();
};

export const getPlanAssignmentsChart = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/coach/charts/plan-assignments`, {
    method: 'GET',
    headers: getAuthHeaders(token),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get plan assignments chart');
  }

  return response.json();
};

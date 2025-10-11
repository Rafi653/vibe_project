import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import * as coachService from '../../services/coachService';
import '../client/ClientDashboard.css';

function CoachDashboard() {
  const { token } = useAuth();
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState(null);
  const [clientProgress, setClientProgress] = useState(null);
  const [showPlanForm, setShowPlanForm] = useState(false);
  const [planType, setPlanType] = useState('workout'); // 'workout' or 'diet'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [workoutPlanForm, setWorkoutPlanForm] = useState({
    user_id: '',
    name: '',
    description: '',
    start_date: new Date().toISOString().split('T')[0],
    duration_weeks: ''
  });

  const [dietPlanForm, setDietPlanForm] = useState({
    user_id: '',
    name: '',
    description: '',
    start_date: new Date().toISOString().split('T')[0],
    target_calories: '',
    target_protein_grams: '',
    target_carbs_grams: '',
    target_fat_grams: ''
  });

  useEffect(() => {
    loadClients();
  }, [token]);

  useEffect(() => {
    if (selectedClient) {
      loadClientProgress(selectedClient.id);
    }
  }, [selectedClient, token]);

  const loadClients = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await coachService.getClients(token);
      setClients(data);
    } catch (err) {
      setError(err.message || 'Failed to load clients');
    } finally {
      setLoading(false);
    }
  };

  const loadClientProgress = async (clientId) => {
    try {
      const data = await coachService.getClientProgress(token, clientId);
      setClientProgress(data);
    } catch (err) {
      console.error('Failed to load client progress:', err);
    }
  };

  const handleWorkoutPlanSubmit = async (e) => {
    e.preventDefault();
    try {
      await coachService.createWorkoutPlan(token, workoutPlanForm);
      setShowPlanForm(false);
      setWorkoutPlanForm({
        user_id: '',
        name: '',
        description: '',
        start_date: new Date().toISOString().split('T')[0],
        duration_weeks: ''
      });
      alert('Workout plan created successfully!');
    } catch (err) {
      setError(err.message || 'Failed to create workout plan');
    }
  };

  const handleDietPlanSubmit = async (e) => {
    e.preventDefault();
    try {
      await coachService.createDietPlan(token, dietPlanForm);
      setShowPlanForm(false);
      setDietPlanForm({
        user_id: '',
        name: '',
        description: '',
        start_date: new Date().toISOString().split('T')[0],
        target_calories: '',
        target_protein_grams: '',
        target_carbs_grams: '',
        target_fat_grams: ''
      });
      alert('Diet plan created successfully!');
    } catch (err) {
      setError(err.message || 'Failed to create diet plan');
    }
  };

  if (loading) {
    return <div className="page-container"><p>Loading dashboard...</p></div>;
  }

  return (
    <div className="page-container">
      <div className="dashboard-header">
        <h1>Coach Dashboard</h1>
        <p>Manage your clients and training programs</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Client Summary */}
      <div className="progress-summary">
        <h2>Your Clients</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>{clients.length}</h3>
            <p>Total Clients</p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <button 
          onClick={() => {
            setPlanType('workout');
            setShowPlanForm(!showPlanForm);
          }} 
          className="primary-button"
        >
          {showPlanForm && planType === 'workout' ? 'Cancel' : 'Create Workout Plan'}
        </button>
        <button 
          onClick={() => {
            setPlanType('diet');
            setShowPlanForm(!showPlanForm);
          }} 
          className="primary-button"
        >
          {showPlanForm && planType === 'diet' ? 'Cancel' : 'Create Diet Plan'}
        </button>
      </div>

      {/* Plan Forms */}
      {showPlanForm && planType === 'workout' && (
        <div className="form-card">
          <h3>Create Workout Plan</h3>
          <form onSubmit={handleWorkoutPlanSubmit}>
            <div className="form-group">
              <label>Client</label>
              <select
                value={workoutPlanForm.user_id}
                onChange={(e) => setWorkoutPlanForm({...workoutPlanForm, user_id: parseInt(e.target.value)})}
                required
              >
                <option value="">Select a client</option>
                {clients.map(client => (
                  <option key={client.id} value={client.id}>
                    {client.full_name} ({client.email})
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Plan Name</label>
              <input
                type="text"
                value={workoutPlanForm.name}
                onChange={(e) => setWorkoutPlanForm({...workoutPlanForm, name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={workoutPlanForm.description}
                onChange={(e) => setWorkoutPlanForm({...workoutPlanForm, description: e.target.value})}
                rows="3"
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Start Date</label>
                <input
                  type="date"
                  value={workoutPlanForm.start_date}
                  onChange={(e) => setWorkoutPlanForm({...workoutPlanForm, start_date: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Duration (weeks)</label>
                <input
                  type="number"
                  value={workoutPlanForm.duration_weeks}
                  onChange={(e) => setWorkoutPlanForm({...workoutPlanForm, duration_weeks: e.target.value})}
                />
              </div>
            </div>
            <button type="submit" className="primary-button">Create Plan</button>
          </form>
        </div>
      )}

      {showPlanForm && planType === 'diet' && (
        <div className="form-card">
          <h3>Create Diet Plan</h3>
          <form onSubmit={handleDietPlanSubmit}>
            <div className="form-group">
              <label>Client</label>
              <select
                value={dietPlanForm.user_id}
                onChange={(e) => setDietPlanForm({...dietPlanForm, user_id: parseInt(e.target.value)})}
                required
              >
                <option value="">Select a client</option>
                {clients.map(client => (
                  <option key={client.id} value={client.id}>
                    {client.full_name} ({client.email})
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Plan Name</label>
              <input
                type="text"
                value={dietPlanForm.name}
                onChange={(e) => setDietPlanForm({...dietPlanForm, name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={dietPlanForm.description}
                onChange={(e) => setDietPlanForm({...dietPlanForm, description: e.target.value})}
                rows="3"
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Start Date</label>
                <input
                  type="date"
                  value={dietPlanForm.start_date}
                  onChange={(e) => setDietPlanForm({...dietPlanForm, start_date: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Target Calories</label>
                <input
                  type="number"
                  value={dietPlanForm.target_calories}
                  onChange={(e) => setDietPlanForm({...dietPlanForm, target_calories: e.target.value})}
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Protein (g)</label>
                <input
                  type="number"
                  value={dietPlanForm.target_protein_grams}
                  onChange={(e) => setDietPlanForm({...dietPlanForm, target_protein_grams: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Carbs (g)</label>
                <input
                  type="number"
                  value={dietPlanForm.target_carbs_grams}
                  onChange={(e) => setDietPlanForm({...dietPlanForm, target_carbs_grams: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Fat (g)</label>
                <input
                  type="number"
                  value={dietPlanForm.target_fat_grams}
                  onChange={(e) => setDietPlanForm({...dietPlanForm, target_fat_grams: e.target.value})}
                />
              </div>
            </div>
            <button type="submit" className="primary-button">Create Plan</button>
          </form>
        </div>
      )}

      {/* Clients List */}
      <div className="recent-logs">
        <h3>Client List</h3>
        <div className="log-list">
          {clients.map((client) => (
            <div 
              key={client.id} 
              className="log-item"
              style={{ cursor: 'pointer' }}
              onClick={() => setSelectedClient(selectedClient?.id === client.id ? null : client)}
            >
              <div className="log-header">
                <strong>{client.full_name}</strong>
                <span>{client.email}</span>
              </div>
              <div className="log-details">
                <span>Status: {client.is_active ? 'Active' : 'Inactive'}</span>
              </div>
              {selectedClient?.id === client.id && clientProgress && (
                <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #ddd' }}>
                  <p><strong>Last 30 Days Activity:</strong></p>
                  <div className="log-details">
                    <span>Workouts: {clientProgress.last_30_days.workout_sessions}</span>
                    <span>Diet Logs: {clientProgress.last_30_days.diet_logs}</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CoachDashboard;

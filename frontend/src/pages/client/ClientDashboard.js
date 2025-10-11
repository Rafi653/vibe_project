import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import * as clientService from '../../services/clientService';
import './ClientDashboard.css';

function ClientDashboard() {
  const { token } = useAuth();
  const [progress, setProgress] = useState(null);
  const [workoutLogs, setWorkoutLogs] = useState([]);
  const [dietLogs, setDietLogs] = useState([]);
  const [showWorkoutForm, setShowWorkoutForm] = useState(false);
  const [showDietForm, setShowDietForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [workoutForm, setWorkoutForm] = useState({
    workout_date: new Date().toISOString().split('T')[0],
    exercise_name: '',
    sets: '',
    reps: '',
    weight: '',
    duration_minutes: '',
    notes: ''
  });

  const [dietForm, setDietForm] = useState({
    meal_date: new Date().toISOString().split('T')[0],
    meal_type: 'breakfast',
    food_name: '',
    calories: '',
    protein_grams: '',
    carbs_grams: '',
    fat_grams: '',
    notes: ''
  });

  useEffect(() => {
    loadDashboardData();
  }, [token]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      const [progressData, workouts, diets] = await Promise.all([
        clientService.getProgress(token),
        clientService.getWorkoutLogs(token),
        clientService.getDietLogs(token)
      ]);
      setProgress(progressData);
      setWorkoutLogs(workouts.slice(0, 5)); // Show latest 5
      setDietLogs(diets.slice(0, 5)); // Show latest 5
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleWorkoutSubmit = async (e) => {
    e.preventDefault();
    try {
      await clientService.createWorkoutLog(token, workoutForm);
      setShowWorkoutForm(false);
      setWorkoutForm({
        workout_date: new Date().toISOString().split('T')[0],
        exercise_name: '',
        sets: '',
        reps: '',
        weight: '',
        duration_minutes: '',
        notes: ''
      });
      loadDashboardData();
    } catch (err) {
      setError(err.message || 'Failed to log workout');
    }
  };

  const handleDietSubmit = async (e) => {
    e.preventDefault();
    try {
      await clientService.createDietLog(token, dietForm);
      setShowDietForm(false);
      setDietForm({
        meal_date: new Date().toISOString().split('T')[0],
        meal_type: 'breakfast',
        food_name: '',
        calories: '',
        protein_grams: '',
        carbs_grams: '',
        fat_grams: '',
        notes: ''
      });
      loadDashboardData();
    } catch (err) {
      setError(err.message || 'Failed to log meal');
    }
  };

  if (loading) {
    return <div className="page-container"><p>Loading dashboard...</p></div>;
  }

  return (
    <div className="page-container">
      <div className="dashboard-header">
        <h1>Client Dashboard</h1>
        <p>Welcome to your personal fitness portal</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Progress Summary */}
      {progress && (
        <div className="progress-summary">
          <h2>Your Progress (Last 30 Days)</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>{progress.last_30_days.workout_sessions}</h3>
              <p>Workout Sessions</p>
            </div>
            <div className="stat-card">
              <h3>{progress.last_30_days.diet_logs}</h3>
              <p>Diet Logs</p>
            </div>
            <div className="stat-card">
              <h3>{progress.active_plans.workout_plans}</h3>
              <p>Active Workout Plans</p>
            </div>
            <div className="stat-card">
              <h3>{progress.active_plans.diet_plans}</h3>
              <p>Active Diet Plans</p>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="action-buttons">
        <button onClick={() => setShowWorkoutForm(!showWorkoutForm)} className="primary-button">
          {showWorkoutForm ? 'Cancel' : 'Log Workout'}
        </button>
        <button onClick={() => setShowDietForm(!showDietForm)} className="primary-button">
          {showDietForm ? 'Cancel' : 'Log Meal'}
        </button>
      </div>

      {/* Workout Form */}
      {showWorkoutForm && (
        <div className="form-card">
          <h3>Log Workout</h3>
          <form onSubmit={handleWorkoutSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Date</label>
                <input
                  type="date"
                  value={workoutForm.workout_date}
                  onChange={(e) => setWorkoutForm({...workoutForm, workout_date: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Exercise Name</label>
                <input
                  type="text"
                  value={workoutForm.exercise_name}
                  onChange={(e) => setWorkoutForm({...workoutForm, exercise_name: e.target.value})}
                  required
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Sets</label>
                <input
                  type="number"
                  value={workoutForm.sets}
                  onChange={(e) => setWorkoutForm({...workoutForm, sets: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Reps</label>
                <input
                  type="number"
                  value={workoutForm.reps}
                  onChange={(e) => setWorkoutForm({...workoutForm, reps: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Weight (kg)</label>
                <input
                  type="number"
                  step="0.1"
                  value={workoutForm.weight}
                  onChange={(e) => setWorkoutForm({...workoutForm, weight: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Duration (min)</label>
                <input
                  type="number"
                  value={workoutForm.duration_minutes}
                  onChange={(e) => setWorkoutForm({...workoutForm, duration_minutes: e.target.value})}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Notes</label>
              <textarea
                value={workoutForm.notes}
                onChange={(e) => setWorkoutForm({...workoutForm, notes: e.target.value})}
                rows="3"
              />
            </div>
            <button type="submit" className="primary-button">Save Workout</button>
          </form>
        </div>
      )}

      {/* Diet Form */}
      {showDietForm && (
        <div className="form-card">
          <h3>Log Meal</h3>
          <form onSubmit={handleDietSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Date</label>
                <input
                  type="date"
                  value={dietForm.meal_date}
                  onChange={(e) => setDietForm({...dietForm, meal_date: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Meal Type</label>
                <select
                  value={dietForm.meal_type}
                  onChange={(e) => setDietForm({...dietForm, meal_type: e.target.value})}
                  required
                >
                  <option value="breakfast">Breakfast</option>
                  <option value="lunch">Lunch</option>
                  <option value="dinner">Dinner</option>
                  <option value="snack">Snack</option>
                </select>
              </div>
              <div className="form-group">
                <label>Food Name</label>
                <input
                  type="text"
                  value={dietForm.food_name}
                  onChange={(e) => setDietForm({...dietForm, food_name: e.target.value})}
                  required
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Calories</label>
                <input
                  type="number"
                  step="0.1"
                  value={dietForm.calories}
                  onChange={(e) => setDietForm({...dietForm, calories: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Protein (g)</label>
                <input
                  type="number"
                  step="0.1"
                  value={dietForm.protein_grams}
                  onChange={(e) => setDietForm({...dietForm, protein_grams: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Carbs (g)</label>
                <input
                  type="number"
                  step="0.1"
                  value={dietForm.carbs_grams}
                  onChange={(e) => setDietForm({...dietForm, carbs_grams: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Fat (g)</label>
                <input
                  type="number"
                  step="0.1"
                  value={dietForm.fat_grams}
                  onChange={(e) => setDietForm({...dietForm, fat_grams: e.target.value})}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Notes</label>
              <textarea
                value={dietForm.notes}
                onChange={(e) => setDietForm({...dietForm, notes: e.target.value})}
                rows="3"
              />
            </div>
            <button type="submit" className="primary-button">Save Meal</button>
          </form>
        </div>
      )}

      {/* Recent Workouts */}
      {workoutLogs.length > 0 && (
        <div className="recent-logs">
          <h3>Recent Workouts</h3>
          <div className="log-list">
            {workoutLogs.map((log) => (
              <div key={log.id} className="log-item">
                <div className="log-header">
                  <strong>{log.exercise_name}</strong>
                  <span>{log.workout_date}</span>
                </div>
                <div className="log-details">
                  {log.sets && log.reps && <span>{log.sets} sets × {log.reps} reps</span>}
                  {log.weight && <span>{log.weight} kg</span>}
                  {log.duration_minutes && <span>{log.duration_minutes} min</span>}
                </div>
                {log.notes && <p className="log-notes">{log.notes}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Diet Logs */}
      {dietLogs.length > 0 && (
        <div className="recent-logs">
          <h3>Recent Meals</h3>
          <div className="log-list">
            {dietLogs.map((log) => (
              <div key={log.id} className="log-item">
                <div className="log-header">
                  <strong>{log.food_name}</strong>
                  <span>{log.meal_date} - {log.meal_type}</span>
                </div>
                <div className="log-details">
                  {log.calories && <span>{log.calories} cal</span>}
                  {log.protein_grams && <span>{log.protein_grams}g protein</span>}
                  {log.carbs_grams && <span>{log.carbs_grams}g carbs</span>}
                  {log.fat_grams && <span>{log.fat_grams}g fat</span>}
                </div>
                {log.notes && <p className="log-notes">{log.notes}</p>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ClientDashboard;

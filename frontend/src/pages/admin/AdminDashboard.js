import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import * as adminService from '../../services/adminService';
import LineChart from '../../components/charts/LineChart';
import BarChart from '../../components/charts/BarChart';
import '../client/ClientDashboard.css';

function AdminDashboard() {
  const { token } = useAuth();
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [showUserEdit, setShowUserEdit] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Chart data states
  const [userGrowthData, setUserGrowthData] = useState(null);
  const [platformUsageData, setPlatformUsageData] = useState(null);
  const [systemHealthData, setSystemHealthData] = useState(null);

  // Feedback data states
  const [feedbackList, setFeedbackList] = useState([]);
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  const [userForm, setUserForm] = useState({
    full_name: '',
    email: '',
    role: 'client',
    is_active: true
  });

  useEffect(() => {
    loadDashboardData();
    loadChartData();
    loadFeedback();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  useEffect(() => {
    loadUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedRole, token]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      const statsData = await adminService.getPlatformStats(token);
      setStats(statsData);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      const usersData = await adminService.getAllUsers(token, selectedRole || null);
      setUsers(usersData);
    } catch (err) {
      console.error('Failed to load users:', err);
    }
  };

  const loadChartData = async () => {
    try {
      const [userGrowth, platformUsage, systemHealth] = await Promise.all([
        adminService.getUserGrowthChart(token, 90),
        adminService.getPlatformUsageChart(token, 30),
        adminService.getSystemHealthChart(token, 7)
      ]);
      setUserGrowthData(userGrowth);
      setPlatformUsageData(platformUsage);
      setSystemHealthData(systemHealth);
    } catch (err) {
      console.error('Failed to load chart data:', err);
    }
  };

  const handleEditUser = (user) => {
    setEditingUser(user);
    setUserForm({
      full_name: user.full_name,
      email: user.email,
      role: user.role,
      is_active: user.is_active
    });
    setShowUserEdit(true);
  };

  const handleUpdateUser = async (e) => {
    e.preventDefault();
    try {
      await adminService.updateUser(token, editingUser.id, userForm);
      setShowUserEdit(false);
      setEditingUser(null);
      loadUsers();
      alert('User updated successfully!');
    } catch (err) {
      setError(err.message || 'Failed to update user');
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await adminService.deleteUser(token, userId);
        loadUsers();
        alert('User deleted successfully!');
      } catch (err) {
        setError(err.message || 'Failed to delete user');
      }
    }
  };

  const loadFeedback = async () => {
    try {
      setFeedbackLoading(true);
      const feedbackData = await adminService.getAllFeedback(token);
      setFeedbackList(feedbackData);
    } catch (err) {
      console.error('Failed to load feedback:', err);
    } finally {
      setFeedbackLoading(false);
    }
  };

  const handleUpdateFeedbackStatus = async (feedbackId, newStatus) => {
    try {
      await adminService.updateFeedbackStatus(token, feedbackId, newStatus);
      loadFeedback();
    } catch (err) {
      setError(err.message || 'Failed to update feedback status');
    }
  };

  const getStatusLabel = (status) => {
    const statusLabels = {
      'open': 'Open',
      'actively_looking': 'Actively Looking Into It',
      'resolved': 'Resolved',
      'cannot_work_on': 'Cannot Work On It'
    };
    return statusLabels[status] || status;
  };

  const getStatusColor = (status) => {
    const statusColors = {
      'open': '#2196F3',
      'actively_looking': '#FF9800',
      'resolved': '#4CAF50',
      'cannot_work_on': '#9E9E9E'
    };
    return statusColors[status] || '#9E9E9E';
  };

  if (loading) {
    return <div className="page-container"><p>Loading dashboard...</p></div>;
  }

  return (
    <div className="page-container">
      <div className="dashboard-header">
        <h1>Admin Dashboard 🛠️</h1>
        <p>System management and oversight 📊</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Platform Statistics */}
      {stats && (
        <div className="progress-summary">
          <h2>📊 Platform Statistics</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>{stats.users.total}</h3>
              <p>👥 Total Users</p>
            </div>
            <div className="stat-card">
              <h3>{stats.users.active}</h3>
              <p>✅ Active Users</p>
            </div>
            <div className="stat-card">
              <h3>{stats.users.clients}</h3>
              <p>💪 Clients</p>
            </div>
            <div className="stat-card">
              <h3>{stats.users.coaches}</h3>
              <p>🏋️ Coaches</p>
            </div>
          </div>

          <h2>📈 Activity (Last 30 Days)</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>{stats.last_30_days.workouts}</h3>
              <p>🏋️ Workout Sessions</p>
            </div>
            <div className="stat-card">
              <h3>{stats.last_30_days.diet_logs}</h3>
              <p>🍎 Diet Logs</p>
            </div>
            <div className="stat-card">
              <h3>{stats.plans.active_workout_plans}</h3>
              <p>💪 Active Workout Plans</p>
            </div>
            <div className="stat-card">
              <h3>{stats.plans.active_diet_plans}</h3>
              <p>🥗 Active Diet Plans</p>
            </div>
          </div>

          <h2>🔥 All Time Activity</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>{stats.activity.total_workouts}</h3>
              <p>🏋️ Total Workouts</p>
            </div>
            <div className="stat-card">
              <h3>{stats.activity.total_diet_logs}</h3>
              <p>🍎 Total Diet Logs</p>
            </div>
          </div>
        </div>
      )}

      {/* Charts Section */}
      <div className="charts-section">
        <h2>📊 Platform Analytics</h2>
        
        {/* User Growth Chart */}
        {userGrowthData && userGrowthData.labels && userGrowthData.labels.length > 0 && (
          <div className="chart-card">
            <h3>📈 User Growth (Last 90 Days)</h3>
            <LineChart
              labels={userGrowthData.labels}
              datasets={[
                {
                  label: 'New Clients',
                  data: userGrowthData.clients,
                  borderColor: 'rgb(97, 218, 251)',
                  backgroundColor: 'rgba(97, 218, 251, 0.2)',
                  fill: true,
                },
                {
                  label: 'New Coaches',
                  data: userGrowthData.coaches,
                  borderColor: 'rgb(255, 159, 64)',
                  backgroundColor: 'rgba(255, 159, 64, 0.2)',
                  fill: true,
                },
                {
                  label: 'New Admins',
                  data: userGrowthData.admins,
                  borderColor: 'rgb(153, 102, 255)',
                  backgroundColor: 'rgba(153, 102, 255, 0.2)',
                  fill: true,
                }
              ]}
            />
          </div>
        )}

        {/* Platform Usage Chart */}
        {platformUsageData && platformUsageData.workouts && platformUsageData.workouts.labels.length > 0 && (
          <div className="chart-card">
            <h3>Platform Activity (Last 30 Days)</h3>
            <BarChart
              labels={platformUsageData.workouts.labels}
              datasets={[
                {
                  label: 'Daily Workouts',
                  data: platformUsageData.workouts.data,
                  backgroundColor: 'rgba(97, 218, 251, 0.7)',
                },
                {
                  label: 'Daily Diet Logs',
                  data: platformUsageData.diet_logs.data,
                  backgroundColor: 'rgba(255, 99, 132, 0.7)',
                }
              ]}
            />
          </div>
        )}

        {/* System Health Chart */}
        {systemHealthData && systemHealthData.daily_active_users && systemHealthData.daily_active_users.labels.length > 0 && (
          <div className="chart-card">
            <h3>System Health (Last 7 Days)</h3>
            <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
              <div className="stat-card">
                <h3>{systemHealthData.total_users}</h3>
                <p>Total Users</p>
              </div>
              <div className="stat-card">
                <h3>{systemHealthData.active_rate.toFixed(1)}%</h3>
                <p>Active Rate</p>
              </div>
            </div>
            <LineChart
              labels={systemHealthData.daily_active_users.labels}
              datasets={[
                {
                  label: 'Daily Active Users',
                  data: systemHealthData.daily_active_users.data,
                  borderColor: 'rgb(75, 192, 192)',
                  backgroundColor: 'rgba(75, 192, 192, 0.2)',
                  fill: true,
                }
              ]}
            />
          </div>
        )}
      </div>

      {/* User Management */}
      <div className="recent-logs">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3>User Management</h3>
          <div className="form-group" style={{ width: '200px', marginBottom: 0 }}>
            <select
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
            >
              <option value="">All Roles</option>
              <option value="client">Clients</option>
              <option value="coach">Coaches</option>
              <option value="admin">Admins</option>
            </select>
          </div>
        </div>

        {/* User Edit Form */}
        {showUserEdit && editingUser && (
          <div className="form-card">
            <h3>Edit User: {editingUser.email}</h3>
            <form onSubmit={handleUpdateUser}>
              <div className="form-group">
                <label>Full Name</label>
                <input
                  type="text"
                  value={userForm.full_name}
                  onChange={(e) => setUserForm({...userForm, full_name: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={userForm.email}
                  onChange={(e) => setUserForm({...userForm, email: e.target.value})}
                  required
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Role</label>
                  <select
                    value={userForm.role}
                    onChange={(e) => setUserForm({...userForm, role: e.target.value})}
                    required
                  >
                    <option value="client">Client</option>
                    <option value="coach">Coach</option>
                    <option value="admin">Admin</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Status</label>
                  <select
                    value={userForm.is_active}
                    onChange={(e) => setUserForm({...userForm, is_active: e.target.value === 'true'})}
                    required
                  >
                    <option value="true">Active</option>
                    <option value="false">Inactive</option>
                  </select>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '1rem' }}>
                <button type="submit" className="primary-button">Update User</button>
                <button 
                  type="button" 
                  className="primary-button" 
                  onClick={() => setShowUserEdit(false)}
                  style={{ backgroundColor: '#666' }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="log-list">
          {users.map((user) => (
            <div key={user.id} className="log-item">
              <div className="log-header">
                <strong>{user.full_name}</strong>
                <span>{user.email}</span>
              </div>
              <div className="log-details">
                <span>Role: {user.role}</span>
                <span>Status: {user.is_active ? 'Active' : 'Inactive'}</span>
                <span>Verified: {user.is_verified ? 'Yes' : 'No'}</span>
              </div>
              <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
                <button 
                  className="primary-button" 
                  onClick={() => handleEditUser(user)}
                  style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}
                >
                  Edit
                </button>
                <button 
                  className="primary-button" 
                  onClick={() => handleDeleteUser(user.id)}
                  style={{ padding: '0.5rem 1rem', fontSize: '0.9rem', backgroundColor: '#c62828' }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Feedback Management */}
      <div className="recent-logs">
        <h3>Feedback Management 💬</h3>
        {feedbackLoading ? (
          <p>Loading feedback...</p>
        ) : feedbackList.length === 0 ? (
          <p>No feedback submissions yet.</p>
        ) : (
          <div className="feedback-table-container">
            <table className="feedback-table">
              <thead>
                <tr>
                  <th>User/Email</th>
                  <th>Message</th>
                  <th>Timestamp</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {feedbackList.map((feedback) => (
                  <tr key={feedback.id}>
                    <td>
                      {feedback.is_anonymous ? (
                        <span style={{ color: '#999' }}>Anonymous</span>
                      ) : (
                        <div>
                          {feedback.name && <div><strong>{feedback.name}</strong></div>}
                          {feedback.email && <div style={{ fontSize: '0.9em', color: '#666' }}>{feedback.email}</div>}
                          {!feedback.name && !feedback.email && <span style={{ color: '#999' }}>No contact info</span>}
                        </div>
                      )}
                    </td>
                    <td>
                      <div style={{ maxWidth: '400px', wordWrap: 'break-word' }}>
                        {feedback.message}
                      </div>
                    </td>
                    <td>
                      <div style={{ fontSize: '0.9em' }}>
                        {new Date(feedback.created_at).toLocaleString()}
                      </div>
                    </td>
                    <td>
                      <span 
                        className="status-badge"
                        style={{ 
                          backgroundColor: getStatusColor(feedback.status),
                          color: 'white',
                          padding: '0.3rem 0.6rem',
                          borderRadius: '4px',
                          fontSize: '0.85em',
                          display: 'inline-block'
                        }}
                      >
                        {getStatusLabel(feedback.status)}
                      </span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <button
                          className="feedback-action-btn"
                          onClick={() => handleUpdateFeedbackStatus(feedback.id, 'actively_looking')}
                          disabled={feedback.status === 'actively_looking'}
                          style={{ 
                            padding: '0.4rem 0.6rem',
                            fontSize: '0.85rem',
                            backgroundColor: feedback.status === 'actively_looking' ? '#ccc' : '#FF9800',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: feedback.status === 'actively_looking' ? 'not-allowed' : 'pointer'
                          }}
                        >
                          👀 Actively Looking
                        </button>
                        <button
                          className="feedback-action-btn"
                          onClick={() => handleUpdateFeedbackStatus(feedback.id, 'resolved')}
                          disabled={feedback.status === 'resolved'}
                          style={{ 
                            padding: '0.4rem 0.6rem',
                            fontSize: '0.85rem',
                            backgroundColor: feedback.status === 'resolved' ? '#ccc' : '#4CAF50',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: feedback.status === 'resolved' ? 'not-allowed' : 'pointer'
                          }}
                        >
                          ✅ Resolved
                        </button>
                        <button
                          className="feedback-action-btn"
                          onClick={() => handleUpdateFeedbackStatus(feedback.id, 'cannot_work_on')}
                          disabled={feedback.status === 'cannot_work_on'}
                          style={{ 
                            padding: '0.4rem 0.6rem',
                            fontSize: '0.85rem',
                            backgroundColor: feedback.status === 'cannot_work_on' ? '#ccc' : '#9E9E9E',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: feedback.status === 'cannot_work_on' ? 'not-allowed' : 'pointer'
                          }}
                        >
                          ❌ Cannot Work On
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;

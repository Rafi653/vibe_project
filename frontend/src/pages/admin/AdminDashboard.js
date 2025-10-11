import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import * as adminService from '../../services/adminService';
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

  const [userForm, setUserForm] = useState({
    full_name: '',
    email: '',
    role: 'client',
    is_active: true
  });

  useEffect(() => {
    loadDashboardData();
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

  if (loading) {
    return <div className="page-container"><p>Loading dashboard...</p></div>;
  }

  return (
    <div className="page-container">
      <div className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <p>System management and oversight</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Platform Statistics */}
      {stats && (
        <div className="progress-summary">
          <h2>Platform Statistics</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>{stats.users.total}</h3>
              <p>Total Users</p>
            </div>
            <div className="stat-card">
              <h3>{stats.users.active}</h3>
              <p>Active Users</p>
            </div>
            <div className="stat-card">
              <h3>{stats.users.clients}</h3>
              <p>Clients</p>
            </div>
            <div className="stat-card">
              <h3>{stats.users.coaches}</h3>
              <p>Coaches</p>
            </div>
          </div>

          <h2>Activity (Last 30 Days)</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>{stats.last_30_days.workouts}</h3>
              <p>Workout Sessions</p>
            </div>
            <div className="stat-card">
              <h3>{stats.last_30_days.diet_logs}</h3>
              <p>Diet Logs</p>
            </div>
            <div className="stat-card">
              <h3>{stats.plans.active_workout_plans}</h3>
              <p>Active Workout Plans</p>
            </div>
            <div className="stat-card">
              <h3>{stats.plans.active_diet_plans}</h3>
              <p>Active Diet Plans</p>
            </div>
          </div>

          <h2>All Time Activity</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>{stats.activity.total_workouts}</h3>
              <p>Total Workouts</p>
            </div>
            <div className="stat-card">
              <h3>{stats.activity.total_diet_logs}</h3>
              <p>Total Diet Logs</p>
            </div>
          </div>
        </div>
      )}

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
    </div>
  );
}

export default AdminDashboard;

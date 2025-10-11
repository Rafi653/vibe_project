import React from 'react';
import '../client/ClientDashboard.css';

function AdminDashboard() {
  return (
    <div className="page-container">
      <div className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <p>System management and oversight</p>
      </div>
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>User Management</h3>
          <p>Manage clients, coaches, and admin accounts</p>
        </div>
        <div className="dashboard-card">
          <h3>System Analytics</h3>
          <p>View platform usage statistics and insights</p>
        </div>
        <div className="dashboard-card">
          <h3>Content Moderation</h3>
          <p>Review and moderate platform content</p>
        </div>
        <div className="dashboard-card">
          <h3>System Settings</h3>
          <p>Configure platform settings and preferences</p>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;

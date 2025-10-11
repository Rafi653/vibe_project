import React from 'react';
import '../client/ClientDashboard.css';

function CoachDashboard() {
  return (
    <div className="page-container">
      <div className="dashboard-header">
        <h1>Coach Dashboard</h1>
        <p>Manage your clients and training programs</p>
      </div>
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>My Clients</h3>
          <p>View and manage your client roster</p>
        </div>
        <div className="dashboard-card">
          <h3>Workout Plans</h3>
          <p>Create and assign personalized workout programs</p>
        </div>
        <div className="dashboard-card">
          <h3>Client Progress</h3>
          <p>Monitor your clients' progress and achievements</p>
        </div>
        <div className="dashboard-card">
          <h3>Schedule</h3>
          <p>Manage your training sessions and appointments</p>
        </div>
      </div>
    </div>
  );
}

export default CoachDashboard;

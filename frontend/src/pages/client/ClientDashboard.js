import React from 'react';
import './ClientDashboard.css';

function ClientDashboard() {
  return (
    <div className="page-container">
      <div className="dashboard-header">
        <h1>Client Dashboard</h1>
        <p>Welcome to your personal fitness portal</p>
      </div>
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>My Workouts</h3>
          <p>View and track your personalized workout plans</p>
        </div>
        <div className="dashboard-card">
          <h3>My Progress</h3>
          <p>Monitor your fitness journey and achievements</p>
        </div>
        <div className="dashboard-card">
          <h3>My Coach</h3>
          <p>Connect with your assigned fitness coach</p>
        </div>
        <div className="dashboard-card">
          <h3>Nutrition Plans</h3>
          <p>Access your customized meal plans and nutrition guidance</p>
        </div>
      </div>
    </div>
  );
}

export default ClientDashboard;

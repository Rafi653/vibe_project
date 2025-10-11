/**
 * Protected Route Component
 * Wraps routes that require authentication and/or specific roles
 */

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function ProtectedRoute({ children, requiredRole }) {
  const { user, loading, isAuthenticated, hasRole } = useAuth();

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontSize: '18px',
        color: '#666'
      }}>
        Loading...
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Check if user has required role
  if (requiredRole && !hasRole(requiredRole)) {
    return (
      <div style={{ 
        padding: '40px', 
        textAlign: 'center',
        color: '#c33'
      }}>
        <h2>Access Denied</h2>
        <p>You don't have permission to access this page.</p>
        <p>Required role: {Array.isArray(requiredRole) ? requiredRole.join(' or ') : requiredRole}</p>
        <p>Your role: {user?.role}</p>
      </div>
    );
  }

  return children;
}

export default ProtectedRoute;

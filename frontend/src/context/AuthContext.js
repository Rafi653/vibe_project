/**
 * Authentication Context for managing user authentication state
 */

import React, { createContext, useState, useContext, useEffect } from 'react';
import { login as loginService, signup as signupService, logout as logoutService, getCurrentUser } from '../services/authService';

const AuthContext = createContext(null);

/**
 * Custom hook to use authentication context
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

/**
 * Authentication Provider Component
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load user on mount if token exists
  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          const userData = await getCurrentUser(token);
          setUser(userData);
        } catch (err) {
          console.error('Failed to load user:', err);
          // If token is invalid, clear it
          localStorage.removeItem('token');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    loadUser();
  }, [token]);

  /**
   * Sign up a new user
   */
  const signup = async (userData) => {
    try {
      setError(null);
      const response = await signupService(userData);
      const { user: newUser, access_token } = response;
      
      // Store token in localStorage
      localStorage.setItem('token', access_token);
      setToken(access_token);
      setUser(newUser);
      
      return { success: true };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    }
  };

  /**
   * Login a user
   */
  const login = async (credentials) => {
    try {
      setError(null);
      const response = await loginService(credentials);
      const { user: loggedInUser, access_token } = response;
      
      // Store token in localStorage
      localStorage.setItem('token', access_token);
      setToken(access_token);
      setUser(loggedInUser);
      
      return { success: true };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    }
  };

  /**
   * Logout the current user
   */
  const logout = async () => {
    try {
      if (token) {
        await logoutService(token);
      }
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      // Always clear local state
      localStorage.removeItem('token');
      setToken(null);
      setUser(null);
      setError(null);
    }
  };

  /**
   * Check if user has a specific role
   */
  const hasRole = (role) => {
    if (!user) return false;
    if (Array.isArray(role)) {
      return role.includes(user.role);
    }
    return user.role === role;
  };

  /**
   * Check if user is admin
   */
  const isAdmin = () => hasRole('admin');

  /**
   * Check if user is coach
   */
  const isCoach = () => hasRole(['coach', 'admin']);

  /**
   * Check if user is client
   */
  const isClient = () => hasRole(['client', 'coach', 'admin']);

  const value = {
    user,
    token,
    loading,
    error,
    signup,
    login,
    logout,
    hasRole,
    isAdmin,
    isCoach,
    isClient,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Signup Component
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Signup.css';

function Signup() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    role: 'client',
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setErrorMessage('Passwords do not match');
      return;
    }

    // Validate password length
    if (formData.password.length < 6) {
      setErrorMessage('Password must be at least 6 characters');
      return;
    }

    setIsLoading(true);

    try {
      const { confirmPassword, ...signupData } = formData;
      const result = await signup(signupData);
      
      if (result.success) {
        // Redirect to home after successful signup
        navigate('/');
      } else {
        setErrorMessage(result.error || 'Signup failed');
      }
    } catch (err) {
      setErrorMessage('An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-card">
        <h2>Join Vibe Fitness</h2>
        
        {errorMessage && (
          <div className="error-message">
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} className="signup-form">
          <div className="form-group">
            <label htmlFor="full_name">Full Name</label>
            <input
              type="text"
              id="full_name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              required
              disabled={isLoading}
              placeholder="John Doe"
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={isLoading}
              placeholder="your.email@example.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={isLoading}
              placeholder="At least 6 characters"
              minLength={6}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              disabled={isLoading}
              placeholder="Re-enter password"
              minLength={6}
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">I am a...</label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              required
              disabled={isLoading}
            >
              <option value="client">Client (looking for coaching)</option>
              <option value="coach">Coach (providing coaching)</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <button type="submit" className="signup-button" disabled={isLoading}>
            {isLoading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <div className="signup-footer">
          <p>
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Signup;

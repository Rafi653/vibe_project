import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import './FeedbackBox.css';

function FeedbackBox() {
  const { user, isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({
    message: '',
    name: '',
    email: '',
    is_anonymous: false
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setIsSubmitting(true);

    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const token = localStorage.getItem('token');
      
      const headers = {
        'Content-Type': 'application/json',
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const payload = {
        message: formData.message,
        name: formData.is_anonymous ? null : (formData.name || (user?.full_name || '')),
        email: formData.is_anonymous ? null : (formData.email || (user?.email || '')),
        is_anonymous: formData.is_anonymous,
        page_url: window.location.href
      };

      const response = await fetch(`${API_BASE_URL}/api/v1/feedback/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to submit feedback');
      }

      setSubmitSuccess(true);
      setFormData({ message: '', name: '', email: '', is_anonymous: false });
      
      setTimeout(() => {
        setSubmitSuccess(false);
        setIsOpen(false);
      }, 3000);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to submit feedback');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <button 
        className="feedback-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Submit Feedback"
      >
        💬 Feedback
      </button>

      {isOpen && (
        <div className="feedback-overlay" onClick={() => setIsOpen(false)}>
          <div className="feedback-modal" onClick={(e) => e.stopPropagation()}>
            <button 
              className="feedback-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close"
            >
              ×
            </button>
            
            <h2>Share Your Feedback</h2>
            <p className="feedback-subtitle">
              Help us improve! Share your suggestions, ideas, or report any issues.
            </p>

            {submitSuccess ? (
              <div className="success-message">
                ✅ Thank you for your feedback! We appreciate your input.
              </div>
            ) : (
              <form onSubmit={handleSubmit}>
                {errorMessage && (
                  <div className="error-message">
                    {errorMessage}
                  </div>
                )}

                <div className="form-group">
                  <label htmlFor="message">Message *</label>
                  <textarea
                    id="message"
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    required
                    disabled={isSubmitting}
                    rows="5"
                    placeholder="Share your thoughts, suggestions, or report issues..."
                  />
                </div>

                {!isAuthenticated && (
                  <>
                    <div className="form-group">
                      <label htmlFor="name">Name (Optional)</label>
                      <input
                        type="text"
                        id="name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        disabled={isSubmitting}
                        placeholder="Your name"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="email">Email (Optional)</label>
                      <input
                        type="email"
                        id="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        disabled={isSubmitting}
                        placeholder="your.email@example.com"
                      />
                    </div>
                  </>
                )}

                {isAuthenticated && (
                  <div className="form-group checkbox-group">
                    <label>
                      <input
                        type="checkbox"
                        checked={formData.is_anonymous}
                        onChange={(e) => setFormData({ ...formData, is_anonymous: e.target.checked })}
                        disabled={isSubmitting}
                      />
                      <span>Submit anonymously</span>
                    </label>
                    {!formData.is_anonymous && (
                      <p className="helper-text">
                        Submitting as {user?.full_name} ({user?.email})
                      </p>
                    )}
                  </div>
                )}

                <button 
                  type="submit" 
                  className="feedback-submit"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </>
  );
}

export default FeedbackBox;

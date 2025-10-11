import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navigation.css';

function Navigation() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <Link to="/">Vibe Fitness</Link>
        </div>
        <ul className="nav-links">
          <li>
            <Link to="/">Home</Link>
          </li>
          {isAuthenticated && (
            <>
              {(user?.role === 'client' || user?.role === 'coach' || user?.role === 'admin') && (
                <li>
                  <Link to="/client">Client Portal</Link>
                </li>
              )}
              {(user?.role === 'coach' || user?.role === 'admin') && (
                <li>
                  <Link to="/coach">Coach Portal</Link>
                </li>
              )}
              {user?.role === 'admin' && (
                <li>
                  <Link to="/admin">Admin Portal</Link>
                </li>
              )}
            </>
          )}
          {!isAuthenticated ? (
            <>
              <li>
                <Link to="/login" className="login-link">Login</Link>
              </li>
              <li>
                <Link to="/signup" className="signup-link">Sign Up</Link>
              </li>
            </>
          ) : (
            <li>
              <button onClick={handleLogout} className="logout-button">
                Logout ({user?.full_name})
              </button>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;

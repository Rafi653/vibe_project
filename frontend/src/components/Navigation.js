import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';

function Navigation() {
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
          <li>
            <Link to="/client">Client Portal</Link>
          </li>
          <li>
            <Link to="/coach">Coach Portal</Link>
          </li>
          <li>
            <Link to="/admin">Admin Portal</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;

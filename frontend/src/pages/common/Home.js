import React from 'react';
import './Home.css';

function Home() {
  return (
    <div className="page-container">
      <div className="home-hero">
        <h1>Welcome to Vibe Fitness 💪</h1>
        <p className="tagline">
          Your journey to a healthier, stronger you starts here ✨
        </p>
        <div className="features">
          <div className="feature-card">
            <div className="feature-icon">🏋️</div>
            <h3>Personalized Coaching</h3>
            <p>Connect with certified fitness coaches and receive tailored workout plans</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Progress Tracking</h3>
            <p>Comprehensive tools for tracking workouts, nutrition, and fitness metrics</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">👥</div>
            <h3>Community Engagement</h3>
            <p>Build a supportive community where you can share your fitness journey</p>
          </div>
        </div>
        <div className="additional-features">
          <div className="mini-feature">
            <span className="mini-icon">🍎</span>
            <span>Nutrition Plans</span>
          </div>
          <div className="mini-feature">
            <span className="mini-icon">💪</span>
            <span>Strength Training</span>
          </div>
          <div className="mini-feature">
            <span className="mini-icon">🔥</span>
            <span>Fat Burn Programs</span>
          </div>
          <div className="mini-feature">
            <span className="mini-icon">🎯</span>
            <span>Goal Setting</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;

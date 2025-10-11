import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  const testimonials = [
    {
      id: 1,
      name: "Sarah Johnson",
      role: "Client",
      image: "👩‍🦰",
      quote: "Vibe Fitness transformed my life! I lost 30 pounds in 6 months and feel stronger than ever. The personalized coaching and nutrition plans made all the difference.",
      rating: 5
    },
    {
      id: 2,
      name: "Mike Chen",
      role: "Client",
      image: "👨",
      quote: "As a busy professional, I struggled to find time for fitness. The flexible workout plans and progress tracking kept me motivated. Down 25 pounds and counting!",
      rating: 5
    },
    {
      id: 3,
      name: "Emily Rodriguez",
      role: "Client",
      image: "👩",
      quote: "The community support here is incredible! Having a coach who understands my goals and the community cheering me on made fitness enjoyable, not a chore.",
      rating: 5
    }
  ];

  const coaches = [
    {
      id: 1,
      name: "Coach Marcus Williams",
      specialty: "Strength & Conditioning",
      image: "🧑‍🏫",
      experience: "10+ years",
      certifications: "NSCA-CSCS, ACE-CPT",
      achievements: "Former collegiate athlete, helped 500+ clients achieve their goals"
    },
    {
      id: 2,
      name: "Coach Lisa Thompson",
      specialty: "Nutrition & Weight Loss",
      image: "👩‍⚕️",
      experience: "8+ years",
      certifications: "RD, NASM-CPT",
      achievements: "Registered Dietitian, specializes in sustainable weight management"
    },
    {
      id: 3,
      name: "Coach David Park",
      specialty: "Functional Fitness",
      image: "👨‍⚕️",
      experience: "12+ years",
      certifications: "CrossFit L2, FMS",
      achievements: "Marathon runner, expert in injury prevention and mobility"
    }
  ];

  return (
    <div className="page-container">
      <div className="home-hero">
        <h1>Welcome to Vibe Fitness 💪</h1>
        <p className="tagline">
          Your journey to a healthier, stronger you starts here ✨
        </p>
        <div className="features">
          <Link to="/features/personalized-coaching" className="feature-card-link">
            <div className="feature-card">
              <div className="feature-icon">🏋️</div>
              <h3>Personalized Coaching</h3>
              <p>Connect with certified fitness coaches and receive tailored workout plans designed specifically for your goals and fitness level.</p>
              <span className="learn-more">Learn More →</span>
            </div>
          </Link>
          <Link to="/features/progress-tracking" className="feature-card-link">
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Progress Tracking</h3>
              <p>Comprehensive tools for tracking workouts, nutrition, and fitness metrics to help you see your improvements over time.</p>
              <span className="learn-more">Learn More →</span>
            </div>
          </Link>
          <Link to="/features/community-engagement" className="feature-card-link">
            <div className="feature-card">
              <div className="feature-icon">👥</div>
              <h3>Community Engagement</h3>
              <p>Build a supportive community where you can share your fitness journey, celebrate victories, and stay motivated together.</p>
              <span className="learn-more">Learn More →</span>
            </div>
          </Link>
        </div>
        <div className="additional-features">
          <Link to="/features/nutrition-plans" className="mini-feature">
            <span className="mini-icon">🍎</span>
            <span>Nutrition Plans</span>
          </Link>
          <Link to="/features/strength-training" className="mini-feature">
            <span className="mini-icon">💪</span>
            <span>Strength Training</span>
          </Link>
          <Link to="/features/fat-burn" className="mini-feature">
            <span className="mini-icon">🔥</span>
            <span>Fat Burn Programs</span>
          </Link>
          <Link to="/features/goal-setting" className="mini-feature">
            <span className="mini-icon">🎯</span>
            <span>Goal Setting</span>
          </Link>
        </div>

        {/* Testimonials Section */}
        <section className="testimonials-section">
          <h2>Success Stories 🌟</h2>
          <p className="section-subtitle">See how Vibe Fitness has transformed lives</p>
          <div className="testimonials-grid">
            {testimonials.map(testimonial => (
              <div key={testimonial.id} className="testimonial-card">
                <div className="testimonial-header">
                  <div className="testimonial-image">{testimonial.image}</div>
                  <div className="testimonial-info">
                    <h4>{testimonial.name}</h4>
                    <p className="testimonial-role">{testimonial.role}</p>
                    <div className="testimonial-rating">
                      {'⭐'.repeat(testimonial.rating)}
                    </div>
                  </div>
                </div>
                <p className="testimonial-quote">"{testimonial.quote}"</p>
              </div>
            ))}
          </div>
        </section>

        {/* Coaches Section */}
        <section className="coaches-section">
          <h2>Meet Our Expert Coaches 👨‍🏫</h2>
          <p className="section-subtitle">Certified professionals dedicated to your success</p>
          <div className="coaches-grid">
            {coaches.map(coach => (
              <div key={coach.id} className="coach-card">
                <div className="coach-image">{coach.image}</div>
                <h3>{coach.name}</h3>
                <p className="coach-specialty">{coach.specialty}</p>
                <div className="coach-details">
                  <p><strong>Experience:</strong> {coach.experience}</p>
                  <p><strong>Certifications:</strong> {coach.certifications}</p>
                  <p className="coach-achievements">{coach.achievements}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Call to Action */}
        <section className="cta-section">
          <h2>Ready to Start Your Journey?</h2>
          <p>Join thousands of others achieving their fitness goals with Vibe Fitness</p>
          <div className="cta-buttons">
            <Link to="/signup" className="cta-button primary">Get Started Free</Link>
            <Link to="/login" className="cta-button secondary">Sign In</Link>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Home;

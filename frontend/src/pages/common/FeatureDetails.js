import React from 'react';
import { useParams, Link } from 'react-router-dom';
import './FeatureDetails.css';

function FeatureDetails() {
  const { featureId } = useParams();

  const features = {
    'personalized-coaching': {
      icon: '🏋️',
      title: 'Personalized Coaching',
      subtitle: 'Expert guidance tailored to your unique fitness journey',
      description: 'Connect with certified fitness coaches who understand your goals and create customized workout plans just for you.',
      benefits: [
        'One-on-one coaching sessions',
        'Customized workout plans based on your fitness level',
        'Regular progress reviews and plan adjustments',
        'Direct messaging with your coach',
        'Video demonstrations and form corrections',
        'Nutritional guidance and meal planning support'
      ],
      howItWorks: [
        'Complete your fitness assessment and set your goals',
        'Get matched with a certified coach that fits your needs',
        'Receive your personalized workout and nutrition plan',
        'Track your progress and communicate with your coach',
        'Adjust and optimize your plan as you progress'
      ]
    },
    'progress-tracking': {
      icon: '📊',
      title: 'Progress Tracking',
      subtitle: 'Comprehensive tools to measure and visualize your fitness journey',
      description: 'Track every aspect of your fitness journey with detailed metrics, charts, and insights that help you stay motivated and on track.',
      benefits: [
        'Log workouts with sets, reps, and weights',
        'Track nutrition with detailed meal logging',
        'Visualize progress with interactive charts',
        'Monitor body measurements and weight changes',
        'Set and track personal records',
        'Export your data for detailed analysis'
      ],
      howItWorks: [
        'Log your daily workouts and meals',
        'View real-time progress charts and statistics',
        'Set milestone goals and track achievements',
        'Review weekly and monthly progress reports',
        'Share achievements with the community'
      ]
    },
    'community-engagement': {
      icon: '👥',
      title: 'Community Engagement',
      subtitle: 'Build connections and find motivation through our supportive community',
      description: 'Join a vibrant community of fitness enthusiasts who support, motivate, and inspire each other to reach their goals.',
      benefits: [
        'Connect with like-minded fitness enthusiasts',
        'Share your progress and celebrate victories',
        'Join challenges and group activities',
        'Get motivation from success stories',
        'Participate in community events and competitions',
        'Find workout buddies in your area'
      ],
      howItWorks: [
        'Create your profile and share your fitness journey',
        'Join groups based on your interests and goals',
        'Participate in challenges and events',
        'Share tips, recipes, and workout ideas',
        'Support and encourage other members'
      ]
    },
    'nutrition-plans': {
      icon: '🍎',
      title: 'Nutrition Plans',
      subtitle: 'Science-based meal plans that fuel your fitness goals',
      description: 'Get personalized nutrition plans designed by registered dietitians to support your training and help you achieve your body composition goals.',
      benefits: [
        'Customized meal plans based on your goals',
        'Macro and calorie tracking',
        'Healthy recipe suggestions',
        'Grocery shopping lists',
        'Meal prep guidance',
        'Dietary restriction accommodations'
      ],
      howItWorks: [
        'Define your nutritional goals and preferences',
        'Receive your personalized meal plan',
        'Log your daily meals and track macros',
        'Adjust plans based on progress and feedback',
        'Access recipes and meal prep tips'
      ]
    },
    'strength-training': {
      icon: '💪',
      title: 'Strength Training',
      subtitle: 'Build muscle and increase strength with progressive training programs',
      description: 'Access comprehensive strength training programs designed to help you build muscle, increase strength, and improve overall fitness.',
      benefits: [
        'Progressive overload training programs',
        'Exercise video library with form tips',
        'Track weights, sets, and reps',
        'Muscle group targeting',
        'Periodization for optimal gains',
        'Rest and recovery guidance'
      ],
      howItWorks: [
        'Start with a strength assessment',
        'Follow your customized lifting program',
        'Track your lifts and progressive overload',
        'Watch form videos for proper technique',
        'Monitor strength gains over time'
      ]
    },
    'fat-burn': {
      icon: '🔥',
      title: 'Fat Burn Programs',
      subtitle: 'High-intensity workouts designed for maximum calorie burn',
      description: 'Burn fat and boost your metabolism with targeted cardio and HIIT programs that deliver results.',
      benefits: [
        'HIIT workout routines',
        'Cardio programming',
        'Metabolic conditioning',
        'Calorie burn tracking',
        'Heart rate zone training',
        'Recovery optimization'
      ],
      howItWorks: [
        'Choose your fat burn program level',
        'Follow guided HIIT and cardio sessions',
        'Track calories burned and heart rate',
        'Combine with nutrition plan for best results',
        'Progress to more challenging routines'
      ]
    },
    'goal-setting': {
      icon: '🎯',
      title: 'Goal Setting',
      subtitle: 'Set SMART goals and track your path to success',
      description: 'Define clear, achievable goals and get the tools and support you need to reach them.',
      benefits: [
        'SMART goal framework',
        'Milestone tracking',
        'Goal-specific action plans',
        'Progress notifications',
        'Achievement badges',
        'Goal accountability features'
      ],
      howItWorks: [
        'Set specific, measurable fitness goals',
        'Break down goals into actionable milestones',
        'Track progress with visual indicators',
        'Receive reminders and motivation',
        'Celebrate achievements and set new goals'
      ]
    }
  };

  const feature = features[featureId];

  if (!feature) {
    return (
      <div className="page-container">
        <div className="feature-not-found">
          <h1>Feature Not Found</h1>
          <p>The feature you're looking for doesn't exist.</p>
          <Link to="/" className="back-link">← Back to Home</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="feature-details">
        <Link to="/" className="back-link">← Back to Home</Link>
        
        <div className="feature-header">
          <div className="feature-icon-large">{feature.icon}</div>
          <h1>{feature.title}</h1>
          <p className="feature-subtitle">{feature.subtitle}</p>
        </div>

        <div className="feature-content">
          <section className="feature-section">
            <h2>Overview</h2>
            <p className="feature-description">{feature.description}</p>
          </section>

          <section className="feature-section">
            <h2>Key Benefits</h2>
            <ul className="benefits-list">
              {feature.benefits.map((benefit, index) => (
                <li key={index}>
                  <span className="benefit-icon">✓</span>
                  {benefit}
                </li>
              ))}
            </ul>
          </section>

          <section className="feature-section">
            <h2>How It Works</h2>
            <ol className="steps-list">
              {feature.howItWorks.map((step, index) => (
                <li key={index}>
                  <span className="step-number">{index + 1}</span>
                  {step}
                </li>
              ))}
            </ol>
          </section>

          <section className="feature-cta">
            <h2>Ready to Get Started?</h2>
            <p>Join Vibe Fitness today and start achieving your goals with {feature.title.toLowerCase()}.</p>
            <div className="cta-buttons">
              <Link to="/signup" className="cta-button primary">Sign Up Now</Link>
              <Link to="/login" className="cta-button secondary">Sign In</Link>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

export default FeatureDetails;

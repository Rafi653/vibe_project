import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navigation from './components/Navigation';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './components/Login';
import Signup from './components/Signup';
import FeedbackBox from './components/FeedbackBox';
import ChatBox from './components/ChatBox';
import Home from './pages/common/Home';
import FeatureDetails from './pages/common/FeatureDetails';
import ClientDashboard from './pages/client/ClientDashboard';
import ClientProfile from './pages/client/ClientProfile';
import CoachDashboard from './pages/coach/CoachDashboard';
import CoachProfile from './pages/coach/CoachProfile';
import AdminDashboard from './pages/admin/AdminDashboard';
import './App.css';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <Navigation />
          <FeedbackBox />
          <ChatBox />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/features/:featureId" element={<FeatureDetails />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              
              {/* Protected Routes */}
              <Route 
                path="/client" 
                element={
                  <ProtectedRoute requiredRole={['client', 'coach', 'admin']}>
                    <ClientDashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/client/profile" 
                element={
                  <ProtectedRoute requiredRole={['client', 'coach', 'admin']}>
                    <ClientProfile />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/coach" 
                element={
                  <ProtectedRoute requiredRole={['coach', 'admin']}>
                    <CoachDashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/coach/profile" 
                element={
                  <ProtectedRoute requiredRole={['coach', 'admin']}>
                    <CoachProfile />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/admin" 
                element={
                  <ProtectedRoute requiredRole="admin">
                    <AdminDashboard />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;

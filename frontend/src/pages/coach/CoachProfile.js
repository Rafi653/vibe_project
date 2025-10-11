import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import * as coachService from '../../services/coachService';
import './CoachProfile.css';

function CoachProfile() {
  const { token } = useAuth();
  const [profile, setProfile] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [formData, setFormData] = useState({
    full_name: '',
    age: '',
    gender: '',
    track_record: '',
    experience: '',
    certifications: '',
    competitions: '',
    qualifications: '',
    specialties: '',
  });

  useEffect(() => {
    fetchProfile();
  }, [token]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await coachService.getProfile(token);
      setProfile(data);
      setFormData({
        full_name: data.full_name || '',
        age: data.age || '',
        gender: data.gender || '',
        track_record: data.track_record || '',
        experience: data.experience || '',
        certifications: data.certifications || '',
        competitions: data.competitions || '',
        qualifications: data.qualifications || '',
        specialties: data.specialties || '',
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      setError('');
      setSuccess('');
      
      // Convert numeric fields
      const dataToSend = {
        ...formData,
        age: formData.age ? parseInt(formData.age) : null,
      };
      
      // Remove empty strings
      Object.keys(dataToSend).forEach(key => {
        if (dataToSend[key] === '' || dataToSend[key] === null) {
          delete dataToSend[key];
        }
      });

      const updated = await coachService.updateProfile(token, dataToSend);
      setProfile(updated);
      setSuccess('Profile updated successfully! 🎉');
      setEditMode(false);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setEditMode(false);
    setError('');
    // Reset form to current profile data
    if (profile) {
      setFormData({
        full_name: profile.full_name || '',
        age: profile.age || '',
        gender: profile.gender || '',
        track_record: profile.track_record || '',
        experience: profile.experience || '',
        certifications: profile.certifications || '',
        competitions: profile.competitions || '',
        qualifications: profile.qualifications || '',
        specialties: profile.specialties || '',
      });
    }
  };

  if (loading) {
    return <div className="page-container"><p>Loading profile...</p></div>;
  }

  return (
    <div className="page-container">
      <div className="profile-header">
        <h1>👨‍🏫 My Coach Profile</h1>
        {!editMode && (
          <button onClick={() => setEditMode(true)} className="primary-button">
            ✏️ Edit Profile
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      {!editMode ? (
        <div className="profile-view">
          <div className="profile-section">
            <h2>📋 Basic Information</h2>
            <div className="profile-grid">
              <div className="profile-field">
                <label>Full Name:</label>
                <span>{profile?.full_name || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Email:</label>
                <span>{profile?.email}</span>
              </div>
              <div className="profile-field">
                <label>Age:</label>
                <span>{profile?.age || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Gender:</label>
                <span>{profile?.gender || 'Not set'}</span>
              </div>
            </div>
          </div>

          <div className="profile-section">
            <h2>🏆 Professional Background</h2>
            <div className="profile-field-full">
              <label>Track Record:</label>
              <p>{profile?.track_record || 'Not set'}</p>
            </div>
            <div className="profile-field-full">
              <label>Experience:</label>
              <p>{profile?.experience || 'Not set'}</p>
            </div>
          </div>

          <div className="profile-section">
            <h2>🎓 Qualifications & Certifications</h2>
            <div className="profile-field-full">
              <label>Certifications:</label>
              <p>{profile?.certifications || 'Not set'}</p>
            </div>
            <div className="profile-field-full">
              <label>Qualifications:</label>
              <p>{profile?.qualifications || 'Not set'}</p>
            </div>
          </div>

          <div className="profile-section">
            <h2>🏅 Achievements & Specialties</h2>
            <div className="profile-field-full">
              <label>Competitions:</label>
              <p>{profile?.competitions || 'Not set'}</p>
            </div>
            <div className="profile-field-full">
              <label>Specialties:</label>
              <p>{profile?.specialties || 'Not set'}</p>
            </div>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="profile-form">
          <div className="profile-section">
            <h2>📋 Basic Information</h2>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="full_name">Full Name *</label>
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="age">Age</label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  min="0"
                  max="150"
                  value={formData.age}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="gender">Gender</label>
                <select
                  id="gender"
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                >
                  <option value="">Select...</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                  <option value="prefer_not_to_say">Prefer not to say</option>
                </select>
              </div>
            </div>
          </div>

          <div className="profile-section">
            <h2>🏆 Professional Background</h2>
            <div className="form-group">
              <label htmlFor="track_record">Track Record</label>
              <textarea
                id="track_record"
                name="track_record"
                rows="3"
                value={formData.track_record}
                onChange={handleChange}
                placeholder="E.g., Trained 200+ clients, 95% client satisfaction rate..."
              />
            </div>
            <div className="form-group">
              <label htmlFor="experience">Experience</label>
              <textarea
                id="experience"
                name="experience"
                rows="3"
                value={formData.experience}
                onChange={handleChange}
                placeholder="E.g., 10 years of professional coaching, worked with athletes and beginners..."
              />
            </div>
          </div>

          <div className="profile-section">
            <h2>🎓 Qualifications & Certifications</h2>
            <div className="form-group">
              <label htmlFor="certifications">Certifications</label>
              <textarea
                id="certifications"
                name="certifications"
                rows="3"
                value={formData.certifications}
                onChange={handleChange}
                placeholder="E.g., NSCA-CSCS, ACE-CPT, Precision Nutrition Level 1..."
              />
            </div>
            <div className="form-group">
              <label htmlFor="qualifications">Qualifications</label>
              <textarea
                id="qualifications"
                name="qualifications"
                rows="3"
                value={formData.qualifications}
                onChange={handleChange}
                placeholder="E.g., BS in Exercise Science, MS in Sports Nutrition..."
              />
            </div>
          </div>

          <div className="profile-section">
            <h2>🏅 Achievements & Specialties</h2>
            <div className="form-group">
              <label htmlFor="competitions">Competitions</label>
              <textarea
                id="competitions"
                name="competitions"
                rows="3"
                value={formData.competitions}
                onChange={handleChange}
                placeholder="E.g., 1st place Regional Bodybuilding Championship 2020..."
              />
            </div>
            <div className="form-group">
              <label htmlFor="specialties">Specialties</label>
              <textarea
                id="specialties"
                name="specialties"
                rows="3"
                value={formData.specialties}
                onChange={handleChange}
                placeholder="E.g., Strength training, weight loss, sports performance, nutrition coaching..."
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="primary-button" disabled={saving}>
              {saving ? '💾 Saving...' : '💾 Save Profile'}
            </button>
            <button type="button" onClick={handleCancel} className="secondary-button" disabled={saving}>
              ❌ Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

export default CoachProfile;

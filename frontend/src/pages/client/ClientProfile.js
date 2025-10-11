import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import * as clientService from '../../services/clientService';
import './ClientProfile.css';

function ClientProfile() {
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
    height: '',
    weight: '',
    bicep_size: '',
    waist: '',
    target_goals: '',
    dietary_restrictions: '',
    health_complications: '',
    injuries: '',
    gym_access: '',
    supplements: '',
    referral_source: '',
  });

  useEffect(() => {
    fetchProfile();
  }, [token]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await clientService.getProfile(token);
      setProfile(data);
      setFormData({
        full_name: data.full_name || '',
        age: data.age || '',
        gender: data.gender || '',
        height: data.height || '',
        weight: data.weight || '',
        bicep_size: data.bicep_size || '',
        waist: data.waist || '',
        target_goals: data.target_goals || '',
        dietary_restrictions: data.dietary_restrictions || '',
        health_complications: data.health_complications || '',
        injuries: data.injuries || '',
        gym_access: data.gym_access || '',
        supplements: data.supplements || '',
        referral_source: data.referral_source || '',
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
        height: formData.height ? parseFloat(formData.height) : null,
        weight: formData.weight ? parseFloat(formData.weight) : null,
        bicep_size: formData.bicep_size ? parseFloat(formData.bicep_size) : null,
        waist: formData.waist ? parseFloat(formData.waist) : null,
      };
      
      // Remove empty strings
      Object.keys(dataToSend).forEach(key => {
        if (dataToSend[key] === '' || dataToSend[key] === null) {
          delete dataToSend[key];
        }
      });

      const updated = await clientService.updateProfile(token, dataToSend);
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
        height: profile.height || '',
        weight: profile.weight || '',
        bicep_size: profile.bicep_size || '',
        waist: profile.waist || '',
        target_goals: profile.target_goals || '',
        dietary_restrictions: profile.dietary_restrictions || '',
        health_complications: profile.health_complications || '',
        injuries: profile.injuries || '',
        gym_access: profile.gym_access || '',
        supplements: profile.supplements || '',
        referral_source: profile.referral_source || '',
      });
    }
  };

  if (loading) {
    return <div className="page-container"><p>Loading profile...</p></div>;
  }

  return (
    <div className="page-container">
      <div className="profile-header">
        <h1>👤 My Profile</h1>
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
            <h2>📏 Body Measurements</h2>
            <div className="profile-grid">
              <div className="profile-field">
                <label>Height (cm):</label>
                <span>{profile?.height || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Weight (kg):</label>
                <span>{profile?.weight || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Bicep Size (cm):</label>
                <span>{profile?.bicep_size || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Waist (cm):</label>
                <span>{profile?.waist || 'Not set'}</span>
              </div>
            </div>
          </div>

          <div className="profile-section">
            <h2>🎯 Fitness Goals & Preferences</h2>
            <div className="profile-field-full">
              <label>Target Goals:</label>
              <p>{profile?.target_goals || 'Not set'}</p>
            </div>
            <div className="profile-field-full">
              <label>Gym Access:</label>
              <p>{profile?.gym_access || 'Not set'}</p>
            </div>
            <div className="profile-field-full">
              <label>Supplements:</label>
              <p>{profile?.supplements || 'Not set'}</p>
            </div>
          </div>

          <div className="profile-section">
            <h2>🏥 Health Information</h2>
            <div className="profile-field-full">
              <label>Dietary Restrictions:</label>
              <p>{profile?.dietary_restrictions || 'Not set'}</p>
            </div>
            <div className="profile-field-full">
              <label>Health Complications:</label>
              <p>{profile?.health_complications || 'Not set'}</p>
            </div>
            <div className="profile-field-full">
              <label>Injuries:</label>
              <p>{profile?.injuries || 'Not set'}</p>
            </div>
          </div>

          <div className="profile-section">
            <h2>ℹ️ Other Information</h2>
            <div className="profile-field-full">
              <label>Referral Source:</label>
              <p>{profile?.referral_source || 'Not set'}</p>
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
            <h2>📏 Body Measurements</h2>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="height">Height (cm)</label>
                <input
                  type="number"
                  id="height"
                  name="height"
                  step="0.1"
                  min="0"
                  value={formData.height}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="weight">Weight (kg)</label>
                <input
                  type="number"
                  id="weight"
                  name="weight"
                  step="0.1"
                  min="0"
                  value={formData.weight}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="bicep_size">Bicep Size (cm)</label>
                <input
                  type="number"
                  id="bicep_size"
                  name="bicep_size"
                  step="0.1"
                  min="0"
                  value={formData.bicep_size}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="waist">Waist (cm)</label>
                <input
                  type="number"
                  id="waist"
                  name="waist"
                  step="0.1"
                  min="0"
                  value={formData.waist}
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>

          <div className="profile-section">
            <h2>🎯 Fitness Goals & Preferences</h2>
            <div className="form-group">
              <label htmlFor="target_goals">Target Goals</label>
              <textarea
                id="target_goals"
                name="target_goals"
                rows="3"
                value={formData.target_goals}
                onChange={handleChange}
                placeholder="E.g., Lose 10kg, build muscle, improve endurance..."
              />
            </div>
            <div className="form-group">
              <label htmlFor="gym_access">Gym Access</label>
              <input
                type="text"
                id="gym_access"
                name="gym_access"
                value={formData.gym_access}
                onChange={handleChange}
                placeholder="E.g., Full gym, home gym, bodyweight only..."
              />
            </div>
            <div className="form-group">
              <label htmlFor="supplements">Supplements</label>
              <textarea
                id="supplements"
                name="supplements"
                rows="2"
                value={formData.supplements}
                onChange={handleChange}
                placeholder="E.g., Protein powder, creatine, vitamins..."
              />
            </div>
          </div>

          <div className="profile-section">
            <h2>🏥 Health Information</h2>
            <div className="form-group">
              <label htmlFor="dietary_restrictions">Dietary Restrictions</label>
              <textarea
                id="dietary_restrictions"
                name="dietary_restrictions"
                rows="2"
                value={formData.dietary_restrictions}
                onChange={handleChange}
                placeholder="E.g., Vegetarian, lactose intolerant, gluten-free..."
              />
            </div>
            <div className="form-group">
              <label htmlFor="health_complications">Health Complications</label>
              <textarea
                id="health_complications"
                name="health_complications"
                rows="2"
                value={formData.health_complications}
                onChange={handleChange}
                placeholder="E.g., Diabetes, heart condition, asthma..."
              />
            </div>
            <div className="form-group">
              <label htmlFor="injuries">Injuries</label>
              <textarea
                id="injuries"
                name="injuries"
                rows="2"
                value={formData.injuries}
                onChange={handleChange}
                placeholder="E.g., Previous knee injury, back pain..."
              />
            </div>
          </div>

          <div className="profile-section">
            <h2>ℹ️ Other Information</h2>
            <div className="form-group">
              <label htmlFor="referral_source">How did you hear about us?</label>
              <input
                type="text"
                id="referral_source"
                name="referral_source"
                value={formData.referral_source}
                onChange={handleChange}
                placeholder="E.g., Friend, social media, advertisement..."
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

export default ClientProfile;

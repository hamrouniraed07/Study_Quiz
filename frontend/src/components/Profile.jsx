import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Profile({ user, onNavigate, apiUrl }) {
  const [stats, setStats] = useState(null);
  const [suggestedDifficulty, setSuggestedDifficulty] = useState(null);

  useEffect(() => {
    loadStats();
    loadSuggestedDifficulty();
  }, []);

  const loadStats = async () => {
    try {
      const response = await axios.get(`${apiUrl}/user-stats/${user.id}`);
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const loadSuggestedDifficulty = async () => {
    try {
      const response = await axios.get(`${apiUrl}/suggest-difficulty/${user.id}`);
      setSuggestedDifficulty(response.data);
    } catch (error) {
      console.error('Error loading difficulty suggestion:', error);
    }
  };

  if (!stats) return <div>Loading...</div>;

  return (
    <>
      <header className="header">
        <h1>👤 Profile</h1>
        <p>{user.username}</p>
      </header>

      <div className="profile-container">
        <div className="profile-stats">
          <h2>Your Statistics</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Total Points</span>
              <span className="stat-value">{user.total_points}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Questions Answered</span>
              <span className="stat-value">{stats.total_questions}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Accuracy</span>
              <span className="stat-value">{stats.accuracy}%</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Study Sessions</span>
              <span className="stat-value">{stats.sessions_count}</span>
            </div>
          </div>
        </div>

        {suggestedDifficulty && (
          <div className="ai-suggestion">
            <h3>🤖 AI Recommendation</h3>
            <p className="difficulty-suggestion">
              Suggested Difficulty: <strong>{suggestedDifficulty.suggested_difficulty.toUpperCase()}</strong>
            </p>
            <p className="suggestion-reason">{suggestedDifficulty.reason}</p>
          </div>
        )}

        <button onClick={() => onNavigate('home')} className="btn btn-primary">
          ← Back to Home
        </button>
      </div>
    </>
  );
}

export default Profile;
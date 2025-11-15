import React, { useState } from 'react';

function Home({ user, leaderboard, onStartQuiz, onNavigate }) {
  const [topic, setTopic] = useState('');
  const [difficulty, setDifficulty] = useState('medium');

  const handleStart = () => {
    if (!topic.trim()) {
      alert('Please enter a topic!');
      return;
    }
    onStartQuiz(topic, difficulty);
  };

  return (
    <>
      <header className="header">
        <h1>📚 StudyPal</h1>
        <p>Your AI-Powered Study Companion</p>
      </header>

      {user && (
        <div className="user-profile-card">
          <div className="user-avatar-large">
            {user.avatar || '🎓'}
          </div>
          <h2>{user.username}</h2>
          <div className="avatar-legend">
            {user.avatar === '👑' && <p>👑 Excellence - Continue comme ça !</p>}
            {user.avatar === '🌟' && <p>🌟 Très bon - Presque parfait !</p>}
            {user.avatar === '🔥' && <p>🔥 Bon niveau - Tu progresses bien !</p>}
            {user.avatar === '💪' && <p>💪 Niveau moyen - Continue tes efforts !</p>}
            {user.avatar === '📚' && <p>📚 En apprentissage - Persévère !</p>}
            {user.avatar === '🌱' && <p>🌱 Débutant - Chaque quiz te fait grandir !</p>}
            {user.avatar === '🎓' && <p>🎓 Nouveau - Bienvenue !</p>}
          </div>
        </div>
      )}

      {user && (
        <div className="user-stats">
          <div className="stat">
            <span className="stat-label">Points</span>
            <span className="stat-value">{user.total_points}</span>
          </div>
          <div className="stat">
            <span className="stat-label">🔥 Streak</span>
            <span className="stat-value">{user.current_streak}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Best Streak</span>
            <span className="stat-value">{user.longest_streak}</span>
          </div>
        </div>
      )}

      <div className="start-quiz">
        <h2>Start a New Quiz</h2>
        <input
          type="text"
          placeholder="Enter a topic (e.g., Python, History, Biology)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="topic-input"
          onKeyPress={(e) => e.key === 'Enter' && handleStart()}
        />

        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="difficulty-select"
        >
          <option value="easy">🟢 Easy - Foundation</option>
          <option value="medium">🟡 Medium - Practice</option>
          <option value="hard">🔴 Hard - Master</option>
        </select>

        <button onClick={handleStart} className="btn btn-primary">
          🚀 Generate AI Questions
        </button>

      
      </div>

      <div className="leaderboard-preview">
        <h2>🏆 Top Students</h2>
        <ol>
          {leaderboard.slice(0, 5).map((u, index) => (
            <li key={u.id} className={u.id === user?.id ? 'highlight' : ''}>
              <span className="rank">
                {index === 0 && '🥇'}
                {index === 1 && '🥈'}
                {index === 2 && '🥉'}
                {index > 2 && `#${index + 1}`}
              </span>
              <span className="user-avatar">{u.avatar || '🎓'}</span>
              <span className="username">{u.username}</span>
              <span className="points">{u.total_points} pts</span>
            </li>
          ))}
        </ol>
        <button onClick={() => onNavigate('leaderboard')} className="btn">
          View Full Leaderboard
        </button>
      </div>
    </>
  );
}

export default Home;
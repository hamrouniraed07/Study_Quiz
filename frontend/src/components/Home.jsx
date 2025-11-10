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
          placeholder="Enter a topic (e.g., World History, Biology, Python Programming)"
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
          <option value="easy">🟢 Easy - Foundation Building</option>
          <option value="medium">🟡 Medium - Practice & Apply</option>
          <option value="hard">🔴 Hard - Master Level</option>
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
              <span className="rank">#{index + 1}</span>
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
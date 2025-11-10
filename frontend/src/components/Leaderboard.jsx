import React from 'react';

function Leaderboard({ leaderboard, currentUser, onNavigate }) {
  return (
    <>
      <header className="header">
        <h1>🏆 Global Leaderboard</h1>
        <p>Top StudyPal Champions</p>
      </header>

      <div className="leaderboard-container">
        <div className="leaderboard-full">
          {leaderboard.length === 0 ? (
            <p className="no-data">No players yet. Be the first!</p>
          ) : (
            <ol>
              {leaderboard.map((user, index) => (
                <li key={user.id} className={user.id === currentUser?.id ? 'highlight' : ''}>
                  <span className="rank">
                    {index === 0 && '🥇'}
                    {index === 1 && '🥈'}
                    {index === 2 && '🥉'}
                    {index > 2 && `#${index + 1}`}
                  </span>
                  <span className="username">{user.username}</span>
                  <div className="user-stats-mini">
                    <span className="points">{user.total_points} pts</span>
                    <span className="streak">{user.current_streak} 🔥</span>
                  </div>
                </li>
              ))}
            </ol>
          )}
          
          <button onClick={() => onNavigate('home')} className="btn btn-primary">
            ← Back to Home
          </button>
        </div>
      </div>
    </>
  );
}

export default Leaderboard;
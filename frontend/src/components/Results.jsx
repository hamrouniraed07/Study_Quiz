import React from 'react';

function Results({ user, quizData, onNavigate }) {
  const totalQuestions = quizData.questions.length;
  const pointsPerCorrect = quizData.difficulty === 'easy' ? 10 : quizData.difficulty === 'medium' ? 20 : 30;
  const correctAnswers = Math.round(quizData.finalScore / pointsPerCorrect);
  const accuracy = ((correctAnswers / totalQuestions) * 100).toFixed(1);

  return (
    <>
      <header className="header">
        <h1>🎉 Quiz Complete!</h1>
      </header>

      <div className="results-container">
        <h2>Great Job, {user.username}!</h2>
        
        <div className="results-grid">
          <div className="result-card">
            <div className="result-icon">📊</div>
            <div className="result-label">Score</div>
            <div className="result-value">{quizData.finalScore} pts</div>
          </div>

          <div className="result-card">
            <div className="result-icon">✅</div>
            <div className="result-label">Correct</div>
            <div className="result-value">{correctAnswers}/{totalQuestions}</div>
          </div>

          <div className="result-card">
            <div className="result-icon">🎯</div>
            <div className="result-label">Accuracy</div>
            <div className="result-value">{accuracy}%</div>
          </div>

          <div className="result-card">
            <div className="result-icon">🔥</div>
            <div className="result-label">Streak</div>
            <div className="result-value">{user.current_streak} days</div>
          </div>
        </div>

        <div className="final-stats">
          <p><strong>Total Points:</strong> {user.total_points}</p>
          <p><strong>Topic:</strong> {quizData.topic}</p>
          <p><strong>Difficulty:</strong> {quizData.difficulty}</p>
        </div>

        <div className="results-actions">
          <button onClick={() => onNavigate('home')} className="btn btn-primary">
            🔄 New Quiz
          </button>
          <button onClick={() => onNavigate('leaderboard')} className="btn">
            🏆 View Leaderboard
          </button>
        </div>
      </div>
    </>
  );
}

export default Results;
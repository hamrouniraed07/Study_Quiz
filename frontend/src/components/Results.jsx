import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Results({ user, quizData, onNavigate, apiUrl }) {
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);
  const [likedQuiz, setLikedQuiz] = useState(null);
  const [showFeedbackQuestion, setShowFeedbackQuestion] = useState(true);

  const totalQuestions = quizData.questions.length;
  const pointsPerCorrect = quizData.difficulty === 'easy' ? 10 : quizData.difficulty === 'medium' ? 20 : 30;
  const correctAnswers = Math.round(quizData.finalScore / pointsPerCorrect);
  const accuracy = ((correctAnswers / totalQuestions) * 100).toFixed(1);

  const handleFeedbackChoice = async (liked) => {
    setLikedQuiz(liked);
    setShowFeedbackQuestion(false);
    setLoading(true);

    try {
      const response = await axios.post(`${apiUrl}/quiz-feedback/`, {
        user_id: user.id,
        topic: quizData.topic,
        score: correctAnswers,
        total_questions: totalQuestions,
        difficulty: quizData.difficulty,
        liked_quiz: liked
      });

      setFeedback(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Erreur feedback:', error);
      setFeedback({
        ai_feedback: "Merci pour ta participation ! Continue à t'entraîner ! 🚀",
        bonus_points: 0,
        bonus_given: false
      });
      setLoading(false);
    }
  };

  return (
    <>
      <header className="header">
        <h1>🎉 Quiz Terminé !</h1>
      </header>

      <div className="results-container">
        <h2>Bravo, {user.username} !</h2>
        
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
            <div className="result-label">Précision</div>
            <div className="result-value">{accuracy}%</div>
          </div>

          <div className="result-card">
            <div className="result-icon">🔥</div>
            <div className="result-label">Streak</div>
            <div className="result-value">{user.current_streak} jours</div>
          </div>
        </div>

        <div className="final-stats">
          <p><strong>Total Points :</strong> {user.total_points}</p>
          <p><strong>Sujet :</strong> {quizData.topic}</p>
          <p><strong>Difficulté :</strong> {quizData.difficulty}</p>
        </div>

        {/* Question de feedback */}
        {showFeedbackQuestion && (
          <div className="feedback-question">
            <h3>💭 Comment s'est passé ce quiz ?</h3>
            <p>As-tu aimé ce quiz et ton score ?</p>
            <div className="feedback-buttons">
              <button 
                onClick={() => handleFeedbackChoice(true)}
                className="btn feedback-btn feedback-yes"
              >
                👍 Oui, c'était bien !
              </button>
              <button 
                onClick={() => handleFeedbackChoice(false)}
                className="btn feedback-btn feedback-no"
              >
                👎 Non, c'était difficile
              </button>
            </div>
          </div>
        )}

        {/* Feedback de l'IA */}
        {!showFeedbackQuestion && (
          <div className="ai-feedback-container">
            {loading ? (
              <div className="loading-feedback">
                <div className="spinner"></div>
                <p>🤖 L'IA génère ton feedback personnalisé...</p>
              </div>
            ) : feedback && (
              <div className="ai-feedback">
                <h3>🤖 Feedback Personnalisé</h3>
                <div className="feedback-content">
                  <p className="feedback-text">{feedback.ai_feedback}</p>
                  
                  {feedback.bonus_given && (
                    <div className="bonus-alert">
                      <span className="bonus-icon">🎁</span>
                      <div>
                        <strong>+{feedback.bonus_points} points bonus !</strong>
                        <p>{feedback.bonus_reason}</p>
                      </div>
                    </div>
                  )}

                  {feedback.suggestion_message && (
                    <div className="suggestion-box">
                      <span className="suggestion-icon">💡</span>
                      <p>{feedback.suggestion_message}</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="results-actions">
          <button onClick={() => onNavigate('home')} className="btn btn-primary">
            🔄 Nouveau Quiz
          </button>
          <button onClick={() => onNavigate('leaderboard')} className="btn">
            🏆 Classement
          </button>
        </div>
      </div>
    </>
  );
}

export default Results;
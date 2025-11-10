import React, { useState } from 'react';
import axios from 'axios';

function QuizGame({ user, quizData, onFinish, onRefreshUser, apiUrl }) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [isCorrect, setIsCorrect] = useState(false);

  const question = quizData.questions[currentQuestion];

  const submitAnswer = async () => {
    if (!selectedAnswer) {
      alert('Please select an answer!');
      return;
    }

    try {
      const response = await axios.post(`${apiUrl}/evaluate-answer/`, {
        user_id: user.id,
        question: question.question,
        user_answer: selectedAnswer,
        correct_answer: question.correct_answer,
        topic: quizData.topic,
        difficulty: quizData.difficulty
      });

      const correct = response.data.is_correct;
      setIsCorrect(correct);

      if (correct) {
        setScore(score + response.data.points_earned);
      }

      setShowResult(true);
      await onRefreshUser();

    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Error submitting answer. Please try again.');
    }
  };

  const nextQuestion = () => {
    setShowResult(false);
    setSelectedAnswer('');
    
    if (currentQuestion < quizData.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      onFinish(score);
    }
  };

  return (
    <>
      <header className="header">
        <h1>📚 {quizData.topic}</h1>
        <div className="quiz-progress">
          Question {currentQuestion + 1} of {quizData.questions.length}
        </div>
        <div className="quiz-score">
          Score: {score} points
        </div>
      </header>

      <div className="quiz-container">
        <div className="difficulty-badge difficulty-{quizData.difficulty}">
          {quizData.difficulty.toUpperCase()}
        </div>

        <h2>{question.question}</h2>

        <div className="options">
          {question.options.map((option, index) => (
            <button
              key={index}
              className={`option-btn ${selectedAnswer === option ? 'selected' : ''} ${
                showResult && option === question.correct_answer ? 'correct-answer' : ''
              } ${
                showResult && selectedAnswer === option && !isCorrect ? 'wrong-answer' : ''
              }`}
              onClick={() => !showResult && setSelectedAnswer(option)}
              disabled={showResult}
            >
              {option}
            </button>
          ))}
        </div>

        {showResult && (
          <div className={`result ${isCorrect ? 'correct' : 'incorrect'}`}>
            {isCorrect ? (
              <div>
                <h3>✅ Correct!</h3>
                <p><strong>Explanation:</strong> {question.explanation}</p>
              </div>
            ) : (
              <div>
                <h3>❌ Not quite!</h3>
                <p><strong>Correct answer:</strong> {question.correct_answer}</p>
                <p><strong>Explanation:</strong> {question.explanation}</p>
              </div>
            )}
            <button onClick={nextQuestion} className="btn btn-primary">
              {currentQuestion < quizData.questions.length - 1 ? 'Next Question →' : 'Finish Quiz 🎉'}
            </button>
          </div>
        )}

        {!showResult && (
          <button onClick={submitAnswer} className="btn btn-primary">
            Submit Answer
          </button>
        )}
      </div>
    </>
  );
}

export default QuizGame;
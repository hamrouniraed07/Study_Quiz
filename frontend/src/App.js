import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Home from './components/Home';
import QuizGame from './components/QuizGame';
import Results from './components/Results';
import Leaderboard from './components/Leaderboard';
import Profile from './components/Profile';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('home');
  const [quizData, setQuizData] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    createDemoUser();
    loadLeaderboard();
  }, []);

  const createDemoUser = async () => {
    try {
      const response = await axios.post(`${API_URL}/users/`, {
        username: `Student${Math.floor(Math.random() * 10000)}`,
        email: `student${Math.floor(Math.random() * 10000)}@studypal.com`
      });
      setUser(response.data);
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  const loadLeaderboard = async () => {
    try {
      const response = await axios.get(`${API_URL}/leaderboard/`);
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error loading leaderboard:', error);
    }
  };

  const refreshUser = async () => {
    if (!user) return;
    try {
      const response = await axios.get(`${API_URL}/users/${user.id}`);
      setUser(response.data);
    } catch (error) {
      console.error('Error refreshing user:', error);
    }
  };

  const startQuiz = async (topic, difficulty) => {
    try {
      const response = await axios.post(`${API_URL}/generate-questions/`, {
        topic,
        difficulty,
        num_questions: 5
      });
      
      setQuizData({
        topic,
        difficulty,
        questions: response.data.questions
      });
      setCurrentView('quiz');
    } catch (error) {
      console.error('Error generating questions:', error);
      alert('Error generating questions. Please check console and try again.');
    }
  };

  const finishQuiz = (finalScore) => {
    setQuizData({ ...quizData, finalScore });
    setCurrentView('results');
    refreshUser();
    loadLeaderboard();
  };

  const navigateTo = (view) => {
    setCurrentView(view);
    if (view === 'leaderboard') {
      loadLeaderboard();
    }
  };

  return (
    <div className="App">
      {currentView === 'home' && (
        <Home 
          user={user}
          leaderboard={leaderboard}
          onStartQuiz={startQuiz}
          onNavigate={navigateTo}
        />
      )}

      {currentView === 'quiz' && quizData && (
        <QuizGame
          user={user}
          quizData={quizData}
          onFinish={finishQuiz}
          onRefreshUser={refreshUser}
          apiUrl={API_URL}
        />
      )}

     {currentView === 'results' && quizData && (
  <Results
    user={user}
    quizData={quizData}
    onNavigate={navigateTo}
    apiUrl={API_URL}  // ← Ajoutez cette ligne
  />
)}

      {currentView === 'leaderboard' && (
        <Leaderboard
          leaderboard={leaderboard}
          currentUser={user}
          onNavigate={navigateTo}
        />
      )}

      {currentView === 'profile' && (
        <Profile
          user={user}
          onNavigate={navigateTo}
          apiUrl={API_URL}
        />
      )}
    </div>
  );
}

export default App;
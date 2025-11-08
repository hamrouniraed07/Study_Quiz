# StudyPal - AI-Powered Quiz Game

StudyPal is an intelligent, gamified learning platform that uses AI to create personalized quiz experiences. Built with FastAPI backend and React frontend, it adapts to user performance and provides engaging educational content across various topics.

## 🚀 Features

### AI-Powered Learning
- **Dynamic Question Generation**: Uses OpenAI GPT to create contextually relevant questions
- **Adaptive Difficulty**: Automatically adjusts question difficulty based on user performance
- **Personalized Learning Paths**: Analyzes user patterns to suggest optimal study strategies

### Gamification Elements
- **Point System**: Earn points based on difficulty and accuracy
- **Streak Tracking**: Maintain daily study streaks for motivation
- **Leaderboards**: Compete with other learners globally
- **Achievements**: Unlock badges for milestones and accomplishments

### User Experience
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Feedback**: Instant answer evaluation with detailed explanations
- **Progress Tracking**: Comprehensive statistics and performance analytics
- **User Profiles**: Personalized dashboard with learning history

## 🛠 Tech Stack

### Backend
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for development
- **OpenAI API**: AI-powered question generation
- **Pydantic**: Data validation and serialization

### Frontend
- **React**: Modern JavaScript library for UI
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing
- **CSS**: Custom styling for responsive design

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- OpenAI API Key

## 🔧 Installation & Setup

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StudyPal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create a `.env` file in the Backend directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./studypal.db
   ```

5. **Run the backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## 📖 Usage

### Starting a Quiz
1. Select a topic from the home page
2. Choose difficulty level (Easy, Medium, Hard)
3. Answer questions and receive instant feedback
4. View results and track progress

### Features Overview
- **Home**: Dashboard with quick stats and quiz options
- **Quiz Game**: Interactive question interface
- **Results**: Detailed performance analysis
- **Leaderboard**: Global ranking system
- **Profile**: Personal statistics and achievements

## 🔌 API Endpoints

### User Management
- `POST /api/users/` - Create new user
- `GET /api/users/{user_id}` - Get user details

### Quiz System
- `POST /api/generate-questions/` - Generate AI-powered questions
- `POST /api/evaluate-answer/` - Submit and evaluate answers
- `GET /api/suggest-difficulty/{user_id}` - Get adaptive difficulty suggestion

### Analytics
- `GET /api/leaderboard/` - Get global leaderboard
- `GET /api/user-stats/{user_id}` - Get user statistics

## 🗄 Database Schema

### Users Table
- User profiles with points, streaks, and achievements

### Study Sessions Table
- Records of quiz attempts with performance metrics

### Achievements System
- Badge system for gamification (future feature)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write descriptive commit messages
- Add tests for new features

## 📝 Future Enhancements

- [ ] Multi-language support
- [ ] Social features (study groups, challenges)
- [ ] Advanced analytics dashboard
- [ ] Mobile app development
- [ ] Integration with learning management systems
- [ ] Custom question bank uploads

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the AI question generation capabilities
- FastAPI and React communities for excellent documentation
- All contributors who help improve StudyPal

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

---

**Happy Learning with StudyPal! 🎓**

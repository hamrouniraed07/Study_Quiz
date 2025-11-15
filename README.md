# StudyPal - AI-Powered Quiz Game 🎓

StudyPal is an intelligent, gamified learning platform that uses **local AI (Ollama)** to create personalized quiz experiences. Built with FastAPI backend and React frontend, it adapts to user performance, provides AI-generated feedback, and features a dynamic avatar system based on learning progress.

## 🚀 Features

### 🤖 AI-Powered Learning (100% Local & Free)
- **Dynamic Question Generation**: Uses Ollama (Llama 3.2) to create contextually relevant questions
- **AI Feedback System**: Personalized post-quiz feedback with encouragement and improvement suggestions
- **Adaptive Difficulty**: Automatically adjusts question difficulty based on user performance
- **Performance-Based Avatars**: Dynamic avatar system that evolves with user accuracy

### 🎮 Gamification Elements
- **Point System**: Earn points based on difficulty (Easy: 10pts, Medium: 20pts, Hard: 30pts)
- **Streak Tracking**: Maintain daily study streaks for motivation
- **Leaderboards**: Compete with other learners globally
- **Avatar Evolution**: 7 different avatars representing skill levels (🎓 → 👑)
- **Bonus Points**: Encouragement points for students facing difficulties

### 🎭 Avatar System
| Avatar | Accuracy | Level |
|--------|----------|-------|
| 👑 | 90-100% | Excellence - Quiz King |
| 🌟 | 80-89% | Very Good - Rising Star |
| 🔥 | 70-79% | Good Level - On Fire |
| 💪 | 60-69% | Medium - Strong & Determined |
| 📚 | 50-59% | Active Learning |
| 🌱 | 40-49% | Beginner Growing |
| 🎓 | 0-39% | New Learner |

### 💬 AI Feedback Features
- **Post-Quiz Questions**: "Did you like the quiz and your score?"
- **Personalized Responses**: AI generates custom feedback based on performance
- **Bonus Points**: Students struggling get encouragement points (20-30 pts)
- **Actionable Suggestions**: Specific advice to improve in the topic

### 📊 User Experience
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Feedback**: Instant answer evaluation with detailed explanations
- **Progress Tracking**: Comprehensive statistics and performance analytics
- **User Profiles**: Personalized dashboard with learning history and avatar display

## 🛠 Tech Stack

### Backend
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for development
- **Ollama**: Local AI for question generation and feedback (Free & Private)
- **Pydantic**: Data validation and serialization

### Frontend
- **React**: Modern JavaScript library for UI
- **Axios**: HTTP client for API communication
- **CSS3**: Custom styling with gradients and animations
- **Responsive Design**: Mobile-first approach

### AI Models
- **Llama 3.2 (3B)**: Primary model for question generation
- **Phi-3 Mini**: Alternative lightweight model
- **Local Processing**: No external API calls, 100% privacy

## 📋 Prerequisites

- **Ubuntu/Linux** (Recommended)
- **Python 3.8+**
- **Node.js 14+**
- **Ollama** (Local AI server)
- **GPU**: Minimum 2GB VRAM (GTX 1650 Ti or better recommended)
- **RAM**: 8GB minimum, 16GB+ recommended

## 🔧 Installation & Setup

### Step 1: Install Ollama
```bash
# Install Ollama on Ubuntu/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Download the AI model (3B version - lightweight)
ollama pull llama3.2:3b

# Test installation
ollama run llama3.2:3b "Hello"
```

### Step 2: Backend Setup

1. **Clone the repository**
```bash
   git clone https://github.com/hamrouniraed07/StudyPal.git
   cd StudyPal
```

2. **Create virtual environment**
```bash
   cd Backend
   python3 -m venv venv
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install --upgrade pip
   pip install fastapi uvicorn sqlalchemy pydantic python-dotenv requests
   pip freeze > requirements.txt
```

4. **Environment variables**
   Create a `.env` file in the Backend directory:
```env
   # Database
   DATABASE_URL=sqlite:///./studypal.db
   
   # Optional: Ollama configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2:3b
```

5. **Run Ollama server (Terminal 1)**
```bash
   ollama serve
```

6. **Run the backend (Terminal 2)**
```bash
   cd Backend
   source venv/bin/activate
   uvicorn app.main:app --reload
```

### Step 3: Frontend Setup

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
1. Enter a topic (e.g., "Python Programming", "World History", "Biology")
2. Choose difficulty level (Easy, Medium, Hard)
3. Click "🚀 Generate AI Questions" (Questions generated in 10-20 seconds)
4. Answer questions and receive instant feedback with explanations
5. After completing the quiz, answer: "Did you like the quiz?"
   - **Yes** → Get congratulations and advanced tips
   - **No** → Get encouragement, bonus points, and specific advice

### Features Overview
- **Home**: Dashboard with avatar, stats, and quick quiz start
- **Quiz Game**: Interactive question interface with AI-generated content
- **Results**: Performance analysis + AI feedback system
- **Leaderboard**: Global ranking with avatars
- **Profile**: Personal statistics and avatar evolution

## 🔌 API Endpoints

### User Management
- `POST /api/users/` - Create new user
- `GET /api/users/{user_id}` - Get user details with avatar

### Quiz System (AI-Powered)
- `POST /api/generate-questions/` - Generate questions using Ollama AI
- `POST /api/evaluate-answer/` - Submit and evaluate answers (updates avatar)
- `GET /api/suggest-difficulty/{user_id}` - Get adaptive difficulty suggestion
- `POST /api/quiz-feedback/` - Generate personalized AI feedback

### Analytics
- `GET /api/leaderboard/` - Get global leaderboard with avatars
- `GET /api/user-stats/{user_id}` - Get user statistics and avatar info
- `GET /api/health` - Check API and Ollama status

## 🗄 Database Schema

### Users Table
```sql
- id: Primary key
- username: Unique username
- email: Unique email
- total_points: Accumulated points
- current_streak: Days in a row
- longest_streak: Best streak record
- avatar: Performance-based emoji (🎓 to 👑)
- last_study_date: Last activity timestamp
```

### Study Sessions Table
```sql
- id: Primary key
- user_id: Foreign key to Users
- topic: Quiz subject
- questions_answered: Total questions
- correct_answers: Correct responses
- points_earned: Points from session
- difficulty: easy/medium/hard
- created_at: Session timestamp
```

## 🎯 AI Architecture

### Question Generation Agent
```python
Role: Generate contextually relevant questions
Input: Topic + Difficulty
Process: 
  1. Analyze topic and difficulty level
  2. Generate 5 multiple-choice questions
  3. Create plausible distractors
  4. Provide educational explanations
Output: Validated JSON with questions
```

### Feedback Generation Agent
```python
Role: Provide personalized learning feedback
Input: Performance data + User sentiment
Process:
  1. Analyze accuracy and difficulty
  2. Determine user satisfaction
  3. Generate empathetic response
  4. Award bonus points if needed
  5. Suggest optimal difficulty
Output: Motivational feedback + recommendations
```

### Adaptive Difficulty Manager
```python
Role: Adjust difficulty based on performance
Input: Last 5 sessions accuracy
Logic:
  - >85% accuracy → Suggest "hard"
  - 50-85% accuracy → Suggest "medium"
  - <50% accuracy → Suggest "easy"
Output: Difficulty recommendation + reasoning
```

## 🔧 Configuration

### Ollama Model Selection

**For GTX 1650 Ti / 2-4GB VRAM:**
```bash
ollama pull llama3.2:3b  # Recommended (2GB VRAM)
ollama pull phi3:mini    # Alternative (2.3GB VRAM)
```

**For RTX 3060+ / 8GB+ VRAM:**
```bash
ollama pull llama3.2     # Full version (4GB VRAM)
ollama pull mistral      # Alternative (4GB VRAM)
```

Update `backend/app/ollama_client.py`:
```python
ollama = OllamaClient(model="llama3.2:3b")  # Change model here
```

## 🧪 Testing

### Test Ollama Connection
```bash
curl http://localhost:11434/api/tags
```

### Test Backend Health
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "ollama_status": "online",
  "model": "llama3.2:3b"
}
```

### Test Question Generation
```bash
curl -X POST http://localhost:8000/api/generate-questions/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python", "difficulty": "easy", "num_questions": 3}'
```

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
- Test AI responses with various topics and difficulties
- Ensure avatar updates work correctly

## 🐛 Troubleshooting

### Ollama Not Responding
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart Ollama
pkill ollama
ollama serve
```

### JSON Parsing Errors
- Update `ollama_client.py` with improved JSON cleaning
- Reduce prompt complexity
- Lower temperature in generation (0.5 instead of 0.8)

### Slow Question Generation
- Use smaller model: `llama3.2:3b` instead of full version
- Reduce `num_predict` in Ollama options
- Check GPU utilization: `nvidia-smi`

### Database Reset
```bash
cd Backend
rm studypal.db
# Restart backend to recreate database
```

## 📝 Project Documentation

### AI Roles in the System
1. **Question Generator**: Creates educational content dynamically
2. **Feedback Provider**: Analyzes performance and provides guidance
3. **Difficulty Adapter**: Ensures optimal learning progression

### Gamification Psychology
- **Progressive Rewards**: Points increase with difficulty
- **Visual Feedback**: Avatars provide instant status recognition
- **Social Proof**: Leaderboards encourage healthy competition
- **Streak Mechanics**: Daily engagement habit formation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** for providing free, local AI infrastructure
- **Meta AI** for Llama 3.2 model
- **FastAPI** and **React** communities for excellent documentation
- All contributors who help improve StudyPal

## 👨‍💻 Author

**Raed Mohamed Amin Hamrouni**
- GitHub: [@hamrouniraed07](https://github.com/hamrouniraed07)
- Project: Final Year Internship Project
- Institution: École Polytechnique de Sousse

## 📞 Support

For questions or support:
- Open an issue on [GitHub Issues](https://github.com/hamrouniraed07/StudyPal/issues)
- Check the troubleshooting section above
- Ensure Ollama is running: `ollama serve`

---

**🎓 Happy Learning with StudyPal - Powered by Local AI!**

*No API costs • 100% Privacy • Unlimited questions*
```

---

## 📋 Fichiers à Inclure

Créez aussi un `LICENSE` file (MIT License) :
```
MIT License

Copyright (c) 2025 Raed Mohamed Amin Hamrouni

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

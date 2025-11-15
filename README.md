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
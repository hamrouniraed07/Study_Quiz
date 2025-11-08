from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

from . import models, database
from .database import engine, get_db

load_dotenv()

# Debug: Check if API key is loaded
openai_key = os.getenv("OPENAI_API_KEY")
print(f"🔑 OpenAI API Key loaded: {'✅ Yes' if openai_key else '❌ No'}")

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS setup for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
openai_client = OpenAI(api_key=openai_key)

# Pydantic models for requests/responses
from pydantic import BaseModel
from datetime import datetime, timedelta

class UserCreate(BaseModel):
    username: str
    email: str

class QuestionRequest(BaseModel):
    topic: str
    difficulty: str
    num_questions: int = 5

class AnswerSubmit(BaseModel):
    user_id: int
    question: str
    user_answer: str
    correct_answer: str
    topic: str
    difficulty: str

# === USER ROUTES ===
@app.post("/api/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# === AI-POWERED QUESTION GENERATION (OpenAI) ===
@app.post("/api/generate-questions/")
def generate_questions(request: QuestionRequest):
    """
    AI Question Generator using OpenAI GPT
    - Generates contextually relevant questions based on topic
    - Adapts question difficulty (easy/medium/hard)
    - Creates diverse question types
    - Provides educational explanations
    """
    
    difficulty_instructions = {
        "easy": "Create basic, foundational questions suitable for beginners. Focus on definitions and simple concepts. Use clear, straightforward language.",
        "medium": "Create intermediate questions that require understanding and application of concepts. Include scenario-based questions.",
        "hard": "Create advanced questions that require deep analysis, synthesis, and critical thinking. Include complex scenarios and edge cases."
    }
    
    prompt = f"""You are an expert educational AI. Generate exactly {request.num_questions} multiple choice questions about "{request.topic}".

Difficulty Level: {request.difficulty}
Instructions: {difficulty_instructions[request.difficulty]}

CRITICAL: Respond with ONLY valid JSON, no markdown formatting, no backticks, no explanations before or after.

Format (respond with this exact structure):
[
  {{
    "question": "Clear, specific question text here?",
    "options": ["First option", "Second option", "Third option", "Fourth option"],
    "correct_answer": "First option",
    "explanation": "Detailed explanation of why this answer is correct and what concept it teaches"
  }}
]

Requirements:
- Make questions specific and educational
- Ensure options are plausible but clearly distinct
- The correct_answer must EXACTLY match one of the options
- Provide thorough explanations

Generate {request.num_questions} questions now:"""

    try:
        print(f"🤖 Generating {request.num_questions} questions about '{request.topic}' at {request.difficulty} difficulty...")
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Cost-effective model
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert educational AI that generates high-quality quiz questions. Always respond with valid JSON only."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7,  # Balanced creativity
            response_format={"type": "json_object"}  # Force JSON response
        )
        
        response_text = response.choices[0].message.content.strip()
        print(f"✅ Received response from OpenAI")
        
        # Remove markdown code blocks if present (backup cleanup)
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        response_text = response_text.strip()
        
        # Parse JSON
        try:
            # Try direct parse first
            questions_data = json.loads(response_text)
            
            # Handle if response is wrapped in an object
            if isinstance(questions_data, dict) and 'questions' in questions_data:
                questions = questions_data['questions']
            elif isinstance(questions_data, list):
                questions = questions_data
            else:
                raise ValueError("Unexpected JSON structure")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
            print(f"Response was: {response_text[:500]}")
            raise HTTPException(status_code=500, detail="AI returned invalid JSON format")
        
        # Validate structure
        if not isinstance(questions, list) or len(questions) == 0:
            raise ValueError("No questions generated")
        
        for i, q in enumerate(questions):
            if not all(key in q for key in ["question", "options", "correct_answer", "explanation"]):
                print(f"⚠️ Question {i} missing required fields: {q}")
                raise ValueError(f"Question {i} has invalid structure")
            
            if not isinstance(q["options"], list) or len(q["options"]) != 4:
                raise ValueError(f"Question {i} must have exactly 4 options")
            
            if q["correct_answer"] not in q["options"]:
                print(f"⚠️ Correct answer not in options for question {i}")
                # Try to fix by using first option
                q["correct_answer"] = q["options"][0]
        
        print(f"✅ Successfully generated {len(questions)} valid questions")
        return {"questions": questions}
        
    except Exception as e:
        print(f"❌ Error generating questions: {str(e)}")
        
        # Fallback to mock questions if API fails
        print("⚠️ Falling back to mock questions...")
        return generate_mock_questions(request)

# === FALLBACK: MOCK QUESTION GENERATOR ===
def generate_mock_questions(request: QuestionRequest):
    """Fallback mock questions if OpenAI fails"""
    
    mock_questions = {
        "easy": {
            "question_templates": [
                f"What is the basic definition of {request.topic}?",
                f"Which of the following is a fundamental concept in {request.topic}?",
                f"What is the primary purpose of {request.topic}?",
                f"In {request.topic}, what does the term 'basic principle' refer to?",
                f"Which statement best describes {request.topic}?"
            ],
            "explanations": [
                "This is a foundational concept that forms the basis of understanding.",
                "Understanding basic definitions is crucial for building knowledge.",
                "This fundamental principle is essential for beginners.",
                "Core concepts help establish a strong foundation.",
                "Basic knowledge serves as the building block for advanced topics."
            ]
        },
        "medium": {
            "question_templates": [
                f"How would you apply {request.topic} in a real-world scenario?",
                f"What is the relationship between {request.topic} and its applications?",
                f"Which approach is most effective when dealing with {request.topic}?",
                f"In the context of {request.topic}, what strategy would you use?",
                f"What are the implications of {request.topic} in practice?"
            ],
            "explanations": [
                "This requires understanding and application of concepts.",
                "Practical application demonstrates deeper comprehension.",
                "This connects theory with real-world implementation.",
                "Understanding relationships shows intermediate knowledge.",
                "Strategic thinking is essential at this level."
            ]
        },
        "hard": {
            "question_templates": [
                f"Analyze the complex implications of {request.topic} in advanced scenarios.",
                f"How would you critically evaluate different approaches to {request.topic}?",
                f"What are the potential limitations and advantages of {request.topic}?",
                f"Synthesize multiple concepts: How does {request.topic} integrate with other advanced topics?",
                f"What would be the optimal solution when combining {request.topic} with competing priorities?"
            ],
            "explanations": [
                "This requires critical thinking and synthesis of multiple concepts.",
                "Advanced analysis involves evaluating trade-offs and implications.",
                "Deep understanding comes from integrating multiple perspectives.",
                "Expert-level questions demand sophisticated reasoning.",
                "This challenges your ability to think at a system level."
            ]
        }
    }
    
    def generate_options(topic, correct_idx=0):
        options = [
            f"Correct understanding of {topic}",
            f"Common misconception about {topic}",
            f"Partially correct interpretation of {topic}",
            f"Incorrect approach to {topic}"
        ]
        correct = options[0]
        options[correct_idx] = correct
        return options, correct
    
    questions = []
    templates = mock_questions[request.difficulty]["question_templates"]
    explanations = mock_questions[request.difficulty]["explanations"]
    
    for i in range(min(request.num_questions, len(templates))):
        correct_idx = i % 4
        options, correct = generate_options(request.topic, correct_idx)
        
        questions.append({
            "question": templates[i],
            "options": options,
            "correct_answer": correct,
            "explanation": explanations[i]
        })
    
    return {"questions": questions}

# === AI-POWERED ADAPTIVE DIFFICULTY ===
@app.get("/api/suggest-difficulty/{user_id}")
def suggest_difficulty(user_id: int, db: Session = Depends(get_db)):
    """
    AI Agent Role: Adaptive Difficulty Manager
    - Analyzes user performance patterns
    - Calculates accuracy trends
    - Suggests optimal difficulty level
    - Ensures progressive learning
    """
    sessions = db.query(models.StudySession)\
        .filter(models.StudySession.user_id == user_id)\
        .order_by(models.StudySession.created_at.desc())\
        .limit(5)\
        .all()
    
    if not sessions:
        return {
            "suggested_difficulty": "medium",
            "reason": "Starting with medium difficulty for new user"
        }
    
    total_questions = sum(s.questions_answered for s in sessions)
    total_correct = sum(s.correct_answers for s in sessions)
    
    accuracy = total_correct / total_questions if total_questions > 0 else 0
    
    # AI Decision Logic for Adaptive Difficulty
    if accuracy > 0.85:
        return {
            "suggested_difficulty": "hard",
            "reason": f"High accuracy ({accuracy*100:.1f}%) - Ready for harder questions",
            "accuracy": accuracy
        }
    elif accuracy < 0.50:
        return {
            "suggested_difficulty": "easy",
            "reason": f"Building foundation ({accuracy*100:.1f}%) - Let's practice basics",
            "accuracy": accuracy
        }
    else:
        return {
            "suggested_difficulty": "medium",
            "reason": f"Good progress ({accuracy*100:.1f}%) - Continue at this level",
            "accuracy": accuracy
        }

# === AI-POWERED ANSWER EVALUATION ===
@app.post("/api/evaluate-answer/")
def evaluate_answer(answer: AnswerSubmit, db: Session = Depends(get_db)):
    """
    AI Agent Role: Answer Evaluator & Feedback Provider
    - Evaluates answer correctness
    - Calculates dynamic point rewards
    - Updates user progress metrics
    - Manages streak system
    """
    is_correct = answer.user_answer.strip() == answer.correct_answer.strip()
    
    # Dynamic point calculation based on difficulty
    points = 0
    if is_correct:
        points_map = {"easy": 10, "medium": 20, "hard": 30}
        points = points_map.get(answer.difficulty, 10)
    
    # Update user stats with AI-driven progression
    user = db.query(models.User).filter(models.User.id == answer.user_id).first()
    if user:
        user.total_points += points
        
        # Streak management (gamification)
        today = datetime.utcnow().date()
        if user.last_study_date:
            last_date = user.last_study_date.date()
            if last_date == today:
                pass  # Same day
            elif last_date == today - timedelta(days=1):
                user.current_streak += 1
            else:
                user.current_streak = 1
        else:
            user.current_streak = 1
        
        user.longest_streak = max(user.longest_streak, user.current_streak)
        user.last_study_date = datetime.utcnow()
        
        # Update or create study session
        session = db.query(models.StudySession)\
            .filter(models.StudySession.user_id == answer.user_id)\
            .filter(models.StudySession.topic == answer.topic)\
            .order_by(models.StudySession.created_at.desc())\
            .first()
        
        if session and (datetime.utcnow() - session.created_at).seconds < 3600:
            # Same session (within 1 hour)
            session.questions_answered += 1
            if is_correct:
                session.correct_answers += 1
            session.points_earned += points
        else:
            # New session
            new_session = models.StudySession(
                user_id=answer.user_id,
                topic=answer.topic,
                questions_answered=1,
                correct_answers=1 if is_correct else 0,
                points_earned=points,
                difficulty=answer.difficulty
            )
            db.add(new_session)
        
        db.commit()
    
    return {
        "is_correct": is_correct,
        "points_earned": points,
        "total_points": user.total_points,
        "current_streak": user.current_streak
    }

# === LEADERBOARD ===
@app.get("/api/leaderboard/")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.total_points.desc()).limit(10).all()
    return users

# === USER STATS ===
@app.get("/api/user-stats/{user_id}")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    sessions = db.query(models.StudySession)\
        .filter(models.StudySession.user_id == user_id)\
        .all()
    
    total_questions = sum(s.questions_answered for s in sessions)
    total_correct = sum(s.correct_answers for s in sessions)
    accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    return {
        "user": user,
        "total_questions": total_questions,
        "total_correct": total_correct,
        "accuracy": round(accuracy, 1),
        "sessions_count": len(sessions)
    }
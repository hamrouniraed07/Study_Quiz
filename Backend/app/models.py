from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    total_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_study_date = Column(DateTime, nullable=True)
    difficulty_level = Column(String, default="medium")
    avatar = Column(String, default="🎓")  # ✨ NOUVEAU : Avatar par défaut
    created_at = Column(DateTime, default=datetime.utcnow)
    
    study_sessions = relationship("StudySession", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")

# Les autres modèles restent identiques
class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String)
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    points_earned = Column(Integer, default=0)
    difficulty = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="study_sessions")

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    icon = Column(String)
    requirement_type = Column(String)
    requirement_value = Column(Integer)

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="achievements")
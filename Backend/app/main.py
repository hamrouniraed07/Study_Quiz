from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import json
import re

from . import models, database
from .database import engine, get_db
from .ollama_client import OllamaClient

load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="StudyPal API - Powered by Ollama")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama client
ollama = OllamaClient(model="llama3.2:3b")

# Test Ollama connection at startup
@app.on_event("startup")
async def startup_event():
    if ollama.is_alive():
        print("✅ Ollama est en ligne et prêt!")
        # Test de génération
        test = ollama.generate("Say 'OK' if you can hear me", temperature=0.1)
        if test:
            print(f"✅ Test de génération réussi: {test[:50]}...")
    else:
        print("⚠️ ATTENTION: Ollama n'est pas démarré!")
        print("💡 Démarrez-le avec: ollama serve")

# Pydantic models
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

class FeedbackRequest(BaseModel):
    user_id: int
    topic: str
    score: int
    total_questions: int
    difficulty: str
    liked_quiz: bool
    
def calculate_avatar(accuracy):
    """
    Calcule l'avatar basé sur le taux de précision global
    """
    if accuracy >= 90:
        return "👑"  # Roi - Excellence
    elif accuracy >= 80:
        return "🌟"  # Étoile - Très bon
    elif accuracy >= 70:
        return "🔥"  # Feu - Bon
    elif accuracy >= 60:
        return "💪"  # Muscle - Moyen
    elif accuracy >= 50:
        return "📚"  # Livre - Apprentissage
    elif accuracy >= 40:
        return "🌱"  # Pousse - Débutant
    else:
        return "🎓"  # Diplôme - Nouveau



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

@app.post("/api/generate-questions/")
def generate_questions(request: QuestionRequest):
    """
    🤖 Génère des questions ENTIÈREMENT avec l'IA locale (Ollama)
    """
    
    if not ollama.is_alive():
        raise HTTPException(
            status_code=503, 
            detail="Ollama n'est pas disponible. Démarrez-le avec: ollama serve"
        )
    
    difficulty_instructions = {
        "easy": "Questions SIMPLES pour débutants. Vocabulaire facile.",
        "medium": "Questions INTERMÉDIAIRES. Mélange théorie et pratique.",
        "hard": "Questions DIFFICILES. Analyse critique requise."
    }
    
    system_prompt = """Tu es un expert en création de quiz.
RÈGLES ABSOLUES:
- Réponds UNIQUEMENT avec du JSON valide
- N'utilise JAMAIS de backslash (\) dans le texte
- N'utilise JAMAIS de guillemets (") dans le texte des questions
- Utilise des apostrophes simples (') si nécessaire
- Pas de markdown, pas d'explications
- Format JSON strict"""
    
    user_prompt = f"""Génère {request.num_questions} questions sur: {request.topic}

Difficulté: {request.difficulty}
{difficulty_instructions[request.difficulty]}

FORMAT JSON (copie exactement ce format):
[
  {{
    "question": "Question simple et claire?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Explication courte et simple"
  }}
]

IMPORTANT:
- Questions courtes (maximum 100 caractères)
- Pas de caractères spéciaux
- Pas de symboles mathématiques complexes
- Texte simple et direct
- N'utilise PAS de backslash ou guillemets dans les textes

Génère maintenant {request.num_questions} questions:"""

    try:
        print(f"\n{'='*60}")
        print(f"🎯 Génération {request.num_questions} questions: {request.topic}")
        print(f"📊 Difficulté: {request.difficulty}")
        print(f"{'='*60}\n")
        
        # Génération avec température plus basse pour plus de stabilité
        response = ollama.generate(user_prompt, system_prompt=system_prompt, temperature=0.5)
        
        if not response:
            raise HTTPException(
                status_code=503,
                detail="Ollama n'a pas pu générer de réponse"
            )
        
        print(f"📥 Réponse brute reçue ({len(response)} caractères)")
        
        # Nettoyer et extraire le JSON
        json_text = ollama.extract_json(response)
        print(f"🔍 JSON nettoyé ({len(json_text)} caractères)")
        
        # Afficher un extrait pour debug
        print(f"📄 Extrait JSON: {json_text[:200]}...")
        
        # Parser le JSON
        try:
            questions = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON: {e}")
            print(f"📄 JSON problématique:\n{json_text[:500]}...")
            
            # Tentative de réparation automatique
            print("🔧 Tentative de réparation du JSON...")
            
            # Remplacer les problèmes courants
            json_text = json_text.replace("'", "'")  # Apostrophes courbes
            json_text = json_text.replace(""", '"')  # Guillemets courbes
            json_text = json_text.replace(""", '"')
            json_text = json_text.replace("…", "...")  # Ellipses
            
            # Retenter le parsing
            try:
                questions = json.loads(json_text)
                print("✅ JSON réparé avec succès!")
            except:
                raise HTTPException(
                    status_code=500,
                    detail=f"JSON invalide même après réparation. Erreur: {str(e)}"
                )
        
        # Validation
        if not isinstance(questions, list):
            raise HTTPException(
                status_code=500,
                detail="Le format de réponse n'est pas une liste"
            )
        
        if len(questions) == 0:
            raise HTTPException(
                status_code=500,
                detail="Aucune question générée"
            )
        
        # Validation de chaque question
        validated_questions = []
        for i, q in enumerate(questions):
            try:
                # Vérifier les champs requis
                required_fields = ["question", "options", "correct_answer", "explanation"]
                if not all(key in q for key in required_fields):
                    print(f"⚠️ Question {i+1} incomplète, ignorée")
                    continue
                
                # Vérifier 4 options
                if not isinstance(q["options"], list) or len(q["options"]) != 4:
                    print(f"⚠️ Question {i+1} n'a pas 4 options, ignorée")
                    continue
                
                # Nettoyer les textes
                q["question"] = str(q["question"]).strip()
                q["options"] = [str(opt).strip() for opt in q["options"]]
                q["correct_answer"] = str(q["correct_answer"]).strip()
                q["explanation"] = str(q["explanation"]).strip()
                
                # Vérifier que correct_answer est dans options
                if q["correct_answer"] not in q["options"]:
                    print(f"⚠️ Question {i+1}: Correction automatique de la réponse")
                    q["correct_answer"] = q["options"][0]
                
                validated_questions.append(q)
                print(f"✅ Question {i+1}/{len(questions)} validée")
                
            except Exception as e:
                print(f"⚠️ Erreur validation question {i+1}: {e}")
                continue
        
        if len(validated_questions) == 0:
            raise HTTPException(
                status_code=500,
                detail="Aucune question valide après validation"
            )
        
        print(f"\n🎉 {len(validated_questions)} questions validées!")
        print(f"{'='*60}\n")
        
        return {"questions": validated_questions[:request.num_questions]}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur: {str(e)}"
        )
        
        
# === FEEDBACK POST-QUIZ 100% GÉNÉRÉ PAR IA ===
@app.post("/api/quiz-feedback/")
def generate_quiz_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    """
    🤖 Génère un feedback ENTIÈREMENT personnalisé avec l'IA
    Analyse les performances et donne des conseils adaptés
    """
    
    if not ollama.is_alive():
        raise HTTPException(
            status_code=503,
            detail="Ollama non disponible"
        )
    
    user = db.query(models.User).filter(models.User.id == feedback.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    accuracy = (feedback.score / feedback.total_questions) * 100
    
    system_prompt = """Tu es un coach pédagogique bienveillant et motivant.
Tu dois donner un feedback personnalisé à un étudiant après son quiz.
Sois encourageant, spécifique et donne des conseils actionnables.
Réponds en français, en 3-4 phrases maximum."""
    
    if feedback.liked_quiz:
        user_prompt = f"""Un étudiant vient de terminer un quiz sur "{feedback.topic}" avec ces résultats:
- Score: {feedback.score}/{feedback.total_questions} ({accuracy:.1f}%)
- Niveau: {feedback.difficulty}
- Ressenti: Il A AIMÉ le quiz (il s'est senti bien)

Génère un message de feedback qui:
1. Le félicite chaleureusement pour sa performance
2. Souligne ce qu'il a bien fait
3. Donne UN conseil spécifique pour progresser encore plus dans "{feedback.topic}"
4. L'encourage à continuer

Ton feedback (3-4 phrases en français):"""
    
    else:
        user_prompt = f"""Un étudiant vient de terminer un quiz sur "{feedback.topic}" avec ces résultats:
- Score: {feedback.score}/{feedback.total_questions} ({accuracy:.1f}%)
- Niveau: {feedback.difficulty}
- Ressenti: Il N'A PAS AIMÉ le quiz (trop difficile ou frustrant)

Génère un message de feedback qui:
1. Reconnaît son effort et valide ses difficultés
2. Donne 2-3 conseils CONCRETS et ACTIONNABLES pour s'améliorer en "{feedback.topic}"
3. Suggère de commencer par un niveau plus facile si nécessaire
4. L'encourage sans le décourager

Ton feedback (3-4 phrases en français, sois empathique):"""
    
    try:
        print(f"\n{'='*60}")
        print(f"💬 Génération de feedback pour {user.username}")
        print(f"📊 Performance: {accuracy:.1f}% | Aimé: {feedback.liked_quiz}")
        print(f"{'='*60}\n")
        
        ai_feedback = ollama.generate(user_prompt, system_prompt=system_prompt, temperature=0.8)
        
        if not ai_feedback:
            ai_feedback = "Merci d'avoir participé ! Continue à t'entraîner, chaque quiz te fait progresser ! 💪"
        
        ai_feedback = ai_feedback.strip()
        
        # Décision intelligente sur les points bonus
        bonus_points = 0
        should_give_bonus = False
        bonus_reason = ""
        
        if not feedback.liked_quiz:
            if accuracy < 40:
                # Très en difficulté -> gros bonus d'encouragement
                bonus_points = 30
                should_give_bonus = True
                bonus_reason = "Bonus d'encouragement pour ta persévérance! 💪"
            elif accuracy < 60:
                # Moyennement en difficulté -> bonus modéré
                bonus_points = 20
                should_give_bonus = True
                bonus_reason = "Bonus pour ton effort malgré la difficulté! 🌟"
        
        if should_give_bonus:
            user.total_points += bonus_points
            db.commit()
            print(f"🎁 {bonus_points} points bonus donnés!")
        
        # Suggestion de difficulté
        suggested_difficulty = feedback.difficulty
        if accuracy < 40:
            suggested_difficulty = "easy"
        elif accuracy > 85 and feedback.difficulty != "hard":
            suggested_difficulty = "hard" if feedback.difficulty == "medium" else "medium"
        
        print(f"✅ Feedback généré avec succès!")
        print(f"{'='*60}\n")
        
        return {
            "ai_feedback": ai_feedback,
            "bonus_points": bonus_points,
            "bonus_given": should_give_bonus,
            "bonus_reason": bonus_reason,
            "suggested_difficulty": suggested_difficulty,
            "suggestion_message": f"Nous te suggérons le niveau '{suggested_difficulty}' pour ta prochaine session."
        }
        
    except Exception as e:
        print(f"❌ Erreur feedback: {e}")
        return {
            "ai_feedback": "Merci pour ta participation ! Continue à t'entraîner, tu progresses ! 🚀",
            "bonus_points": 0,
            "bonus_given": False,
            "bonus_reason": "",
            "suggested_difficulty": feedback.difficulty,
            "suggestion_message": ""
        }

# === ADAPTIVE DIFFICULTY ===
@app.get("/api/suggest-difficulty/{user_id}")
def suggest_difficulty(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(models.StudySession)\
        .filter(models.StudySession.user_id == user_id)\
        .order_by(models.StudySession.created_at.desc())\
        .limit(5)\
        .all()
    
    if not sessions:
        return {
            "suggested_difficulty": "medium",
            "reason": "Nouveau utilisateur - commence au niveau moyen",
            "accuracy": 0
        }
    
    total_questions = sum(s.questions_answered for s in sessions)
    total_correct = sum(s.correct_answers for s in sessions)
    
    accuracy = total_correct / total_questions if total_questions > 0 else 0
    
    if accuracy > 0.85:
        return {
            "suggested_difficulty": "hard",
            "reason": f"Excellente précision ({accuracy*100:.1f}%) - Tu es prêt pour le niveau difficile! 🚀",
            "accuracy": accuracy
        }
    elif accuracy < 0.50:
        return {
            "suggested_difficulty": "easy",
            "reason": f"Construisons les bases ({accuracy*100:.1f}%) - Le niveau facile t'aidera à progresser 📚",
            "accuracy": accuracy
        }
    else:
        return {
            "suggested_difficulty": "medium",
            "reason": f"Bonne progression ({accuracy*100:.1f}%) - Continue à ce niveau! 💪",
            "accuracy": accuracy
        }

# === ANSWER EVALUATION AVEC MISE À JOUR AVATAR ===
@app.post("/api/evaluate-answer/")
def evaluate_answer(answer: AnswerSubmit, db: Session = Depends(get_db)):
    is_correct = answer.user_answer.strip() == answer.correct_answer.strip()
    
    points = 0
    if is_correct:
        points_map = {"easy": 10, "medium": 20, "hard": 30}
        points = points_map.get(answer.difficulty, 10)
    
    user = db.query(models.User).filter(models.User.id == answer.user_id).first()
    if user:
        user.total_points += points
        
        today = datetime.utcnow().date()
        if user.last_study_date:
            last_date = user.last_study_date.date()
            if last_date == today:
                pass
            elif last_date == today - timedelta(days=1):
                user.current_streak += 1
            else:
                user.current_streak = 1
        else:
            user.current_streak = 1
        
        user.longest_streak = max(user.longest_streak, user.current_streak)
        user.last_study_date = datetime.utcnow()
        
        session = db.query(models.StudySession)\
            .filter(models.StudySession.user_id == answer.user_id)\
            .filter(models.StudySession.topic == answer.topic)\
            .order_by(models.StudySession.created_at.desc())\
            .first()
        
        if session and (datetime.utcnow() - session.created_at).seconds < 3600:
            session.questions_answered += 1
            if is_correct:
                session.correct_answers += 1
            session.points_earned += points
        else:
            new_session = models.StudySession(
                user_id=answer.user_id,
                topic=answer.topic,
                questions_answered=1,
                correct_answers=1 if is_correct else 0,
                points_earned=points,
                difficulty=answer.difficulty
            )
            db.add(new_session)
        
        # ✨ NOUVEAU : Calculer et mettre à jour l'avatar
        all_sessions = db.query(models.StudySession)\
            .filter(models.StudySession.user_id == answer.user_id)\
            .all()
        
        total_questions = sum(s.questions_answered for s in all_sessions)
        total_correct = sum(s.correct_answers for s in all_sessions)
        
        if total_questions > 0:
            global_accuracy = (total_correct / total_questions) * 100
            user.avatar = calculate_avatar(global_accuracy)
            print(f"🎭 Avatar mis à jour pour {user.username}: {user.avatar} (Précision: {global_accuracy:.1f}%)")
        
        db.commit()
    
    return {
        "is_correct": is_correct,
        "points_earned": points,
        "total_points": user.total_points,
        "current_streak": user.current_streak,
        "avatar": user.avatar  # ✨ Retourner l'avatar
    }
# === LEADERBOARD ===
@app.get("/api/leaderboard/")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.total_points.desc()).limit(10).all()
    return users

# === USER STATS AVEC AVATAR ===
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
    
    # ✨ Mettre à jour l'avatar basé sur l'accuracy actuelle
    user.avatar = calculate_avatar(accuracy)
    db.commit()
    
    return {
        "user": user,
        "total_questions": total_questions,
        "total_correct": total_correct,
        "accuracy": round(accuracy, 1),
        "sessions_count": len(sessions),
        "avatar": user.avatar  # ✨ Inclure l'avatar
    }
# === HEALTH CHECK ===
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "ollama_status": "online" if ollama.is_alive() else "offline",
        "model": ollama.model
    }
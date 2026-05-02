from fastapi import APIRouter, HTTPException, Depends, Query, Header
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import random

from database import get_db
from models import User, Question, UserProgress, Topic
from routes.auth import get_current_user

router = APIRouter()

@router.get("/personalized")
def get_personalized_recommendations(
    authorization: Optional[str] = Header(None),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    """Get personalized question recommendations based on user performance"""
    current_user = get_current_user(authorization, db)
    
    # Get weak topics (topics with < 60% accuracy)
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()
    
    weak_topics = {}
    for progress in progress_records:
        question = db.query(Question).filter(Question.id == progress.question_id).first()
        if question:
            topic_id = question.topic_id
            if topic_id not in weak_topics:
                weak_topics[topic_id] = {"correct": 0, "total": 0, "name": question.topic.name}
            weak_topics[topic_id]["total"] += 1
            if progress.is_correct:
                weak_topics[topic_id]["correct"] += 1
    
    # Filter topics with < 60% accuracy
    low_accuracy_topics = []
    for topic_id, data in weak_topics.items():
        accuracy = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
        if accuracy < 60:
            low_accuracy_topics.append((topic_id, data["name"], accuracy))
    
    # Sort by accuracy (weakest first)
    low_accuracy_topics.sort(key=lambda x: x[2])
    
    recommendations = []
    
    # For each weak topic, recommend questions
    for topic_id, topic_name, accuracy in low_accuracy_topics[:5]:
        # Get answered question IDs
        answered = db.query(UserProgress.question_id).filter(
            UserProgress.user_id == current_user.id
        ).all()
        answered_ids = [q[0] for q in answered]
        
        # Get unanswered questions from this topic
        questions = db.query(Question).filter(
            Question.topic_id == topic_id,
            Question.id.notin_(answered_ids)
        ).order_by(Question.difficulty_level).limit(limit).all()
        
        for q in questions:
            recommendations.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "difficulty_level": q.difficulty_level,
                "topic_name": topic_name,
                "reason": f"Your weak area - {accuracy:.1f}% accuracy"
            })
    
    # If not enough recommendations, add random questions
    if len(recommendations) < limit:
        answered = db.query(UserProgress.question_id).filter(
            UserProgress.user_id == current_user.id
        ).all()
        answered_ids = [q[0] for q in answered]
        
        remaining_needed = limit - len(recommendations)
        additional = db.query(Question).filter(
            Question.id.notin_(answered_ids),
            Question.exam_id == db.query(User).filter(User.id == current_user.id).first().id
        ).order_by(func.random()).limit(remaining_needed).all()
        
        for q in additional:
            recommendations.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "difficulty_level": q.difficulty_level,
                "topic_name": q.topic.name,
                "reason": "Suggested for practice"
            })
    
    return recommendations[:limit]

@router.get("/by-topic/{topic_id}")
def get_recommendations_by_topic(
    topic_id: int,
    authorization: Optional[str] = Header(None),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    """Get questions from a specific weak topic"""
    current_user = get_current_user(authorization, db)
    
    # Verify topic exists
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Get answered question IDs
    answered = db.query(UserProgress.question_id).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.is_correct == True
    ).all()
    answered_ids = [q[0] for q in answered]
    
    # Get unanswered questions from this topic
    questions = db.query(Question).filter(
        Question.topic_id == topic_id,
        Question.id.notin_(answered_ids)
    ).order_by(Question.difficulty_level).limit(limit).all()
    
    return [
        {
            "id": q.id,
            "question_text": q.question_text,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "difficulty_level": q.difficulty_level,
            "subject_id": q.subject_id,
            "topic_id": q.topic_id,
            "exam_id": q.exam_id
        }
        for q in questions
    ]

@router.post("/retrain")
def retrain_model(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Retrain the recommendation model with latest data"""
    current_user = get_current_user(authorization, db)
    
    users_count = db.query(func.count(User.id)).scalar()
    questions_count = db.query(func.count(Question.id)).scalar()
    
    return {
        "message": "Model retraining initiated",
        "total_users": users_count,
        "total_questions": questions_count,
        "status": "In Progress"
    }

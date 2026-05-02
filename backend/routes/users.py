from fastapi import APIRouter, HTTPException, Depends, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime

from database import get_db
from models import UserProgress, Topic, Question
from routes.auth import get_current_user

router = APIRouter()

@router.get("/stats")
def get_user_stats(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get user statistics and weak topics"""
    current_user = get_current_user(authorization, db)
    
    # Get overall stats
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()
    
    total_attempted = len(progress_records)
    total_correct = sum(1 for p in progress_records if p.is_correct)
    accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
    
    # Get weak topics
    weak_topics_data = []
    topics_attempted = {}
    
    for progress in progress_records:
        question = db.query(Question).filter(Question.id == progress.question_id).first()
        if question:
            topic_id = question.topic_id
            if topic_id not in topics_attempted:
                topics_attempted[topic_id] = {"correct": 0, "total": 0, "topic": question.topic}
            topics_attempted[topic_id]["total"] += 1
            if progress.is_correct:
                topics_attempted[topic_id]["correct"] += 1
    
    for topic_id, data in topics_attempted.items():
        topic_accuracy = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
        if topic_accuracy < 60:  # Weak topics have < 60% accuracy
            weak_topics_data.append({
                "topic_id": topic_id,
                "topic_name": data["topic"].name,
                "attempted": data["total"],
                "correct": data["correct"],
                "accuracy_percentage": topic_accuracy
            })
    
    # Sort by accuracy (weakest first)
    weak_topics_data.sort(key=lambda x: x["accuracy_percentage"])
    
    return {
        "total_attempted": total_attempted,
        "total_correct": total_correct,
        "accuracy_percentage": accuracy,
        "weak_topics": weak_topics_data
    }

@router.get("/progress/{question_id}")
def get_question_progress(
    question_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get user's progress on a specific question"""
    current_user = get_current_user(authorization, db)
    
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.question_id == question_id
    ).first()
    
    if not progress:
        return {"attempted": False}
    
    return {
        "attempted": True,
        "is_correct": progress.is_correct,
        "time_spent_seconds": progress.time_spent_seconds,
        "attempted_at": progress.attempted_at.isoformat() if progress.attempted_at else None
    }

@router.get("/history")
def get_attempt_history(
    authorization: Optional[str] = Header(None),
    limit: int = Query(50),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """Get user's question attempt history"""
    current_user = get_current_user(authorization, db)
    
    history = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).order_by(UserProgress.attempted_at.desc()).limit(limit).offset(offset).all()
    
    result = []
    for h in history:
        question = db.query(Question).filter(Question.id == h.question_id).first()
        result.append({
            "id": h.id,
            "question_id": h.question_id,
            "question_text": question.question_text if question else "",
            "difficulty_level": question.difficulty_level if question else "",
            "is_correct": h.is_correct,
            "attempted_at": h.attempted_at.isoformat() if h.attempted_at else None,
            "time_spent_seconds": h.time_spent_seconds
        })
    
    return result

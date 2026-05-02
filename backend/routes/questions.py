from fastapi import APIRouter, HTTPException, Depends, Query, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Question, Bookmark, User, UserProgress
from routes.auth import get_current_user

router = APIRouter()

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty_level: str
    subject_id: int
    topic_id: int
    exam_id: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/")
def get_questions(
    exam_id: Optional[int] = Query(None),
    subject_id: Optional[int] = Query(None),
    topic_id: Optional[int] = Query(None),
    difficulty_level: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    limit: int = Query(20),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """Get questions with filters"""
    query = db.query(Question)
    
    if exam_id:
        query = query.filter(Question.exam_id == exam_id)
    if subject_id:
        query = query.filter(Question.subject_id == subject_id)
    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    if difficulty_level:
        query = query.filter(Question.difficulty_level == difficulty_level)
    if keyword:
        query = query.filter(Question.question_text.ilike(f"%{keyword}%"))
    
    total = query.count()
    questions = query.limit(limit).offset(offset).all()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "questions": [QuestionResponse.from_orm(q) for q in questions]
    }

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get a single question"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("/bookmarks/{question_id}")
def add_bookmark(
    question_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Add question to bookmarks"""
    current_user = get_current_user(authorization, db)
    
    # Check if question exists
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if already bookmarked
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == question_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already bookmarked")
    
    bookmark = Bookmark(user_id=current_user.id, question_id=question_id)
    db.add(bookmark)
    db.commit()
    
    return {"message": "Bookmarked successfully"}

@router.get("/bookmarks/list")
def get_bookmarks(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get user's bookmarked questions"""
    current_user = get_current_user(authorization, db)
    
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()
    return {"bookmarks": [b.question_id for b in bookmarks]}

@router.delete("/bookmarks/{question_id}")
def remove_bookmark(
    question_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Remove question from bookmarks"""
    current_user = get_current_user(authorization, db)
    
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == question_id
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    
    return {"message": "Bookmark removed"}

@router.post("/submit-answer")
def submit_answer(
    question_id: int = Query(...),
    answer_given: str = Query(...),
    time_spent_seconds: int = Query(...),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Submit answer and record progress"""
    current_user = get_current_user(authorization, db)
    
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    is_correct = answer_given == question.correct_answer
    
    # Create or update progress
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.question_id == question_id
    ).first()
    
    if progress:
        progress.answer_given = answer_given
        progress.is_correct = is_correct
        progress.time_spent_seconds = time_spent_seconds
    else:
        progress = UserProgress(
            user_id=current_user.id,
            question_id=question_id,
            answer_given=answer_given,
            is_correct=is_correct,
            time_spent_seconds=time_spent_seconds
        )
        db.add(progress)
    
    db.commit()
    
    return {"is_correct": is_correct, "correct_answer": question.correct_answer}

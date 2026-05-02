from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List
import os

from database import get_db
from models import Exam, Subject, Topic, Question, User, UserProgress

router = APIRouter()

# Admin password
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

def verify_admin(admin_password: str):
    """Simple admin verification"""
    if admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Pydantic models
class ExamCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SubjectCreate(BaseModel):
    exam_id: int
    name: str
    description: Optional[str] = None

class TopicCreate(BaseModel):
    subject_id: int
    name: str
    description: Optional[str] = None

class QuestionCreate(BaseModel):
    exam_id: int
    subject_id: int
    topic_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    explanation: Optional[str] = None
    difficulty_level: str = "medium"

@router.post("/exams")
def create_exam(exam: ExamCreate, admin_password: str = Query(...), db: Session = Depends(get_db)):
    """Create a new exam"""
    verify_admin(admin_password)
    
    # Check if exam already exists
    existing = db.query(Exam).filter(Exam.name == exam.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Exam already exists")
    
    db_exam = Exam(name=exam.name, description=exam.description)
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam

@router.get("/exams")
def get_exams(db: Session = Depends(get_db)):
    """Get all exams"""
    exams = db.query(Exam).all()
    return exams

@router.post("/subjects")
def create_subject(subject: SubjectCreate, admin_password: str = Query(...), db: Session = Depends(get_db)):
    """Create a new subject"""
    verify_admin(admin_password)
    
    # Verify exam exists
    exam = db.query(Exam).filter(Exam.id == subject.exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    db_subject = Subject(exam_id=subject.exam_id, name=subject.name, description=subject.description)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/subjects")
def get_subjects(exam_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get all subjects"""
    query = db.query(Subject)
    if exam_id:
        query = query.filter(Subject.exam_id == exam_id)
    return query.all()

@router.post("/topics")
def create_topic(topic: TopicCreate, admin_password: str = Query(...), db: Session = Depends(get_db)):
    """Create a new topic"""
    verify_admin(admin_password)
    
    # Verify subject exists
    subject = db.query(Subject).filter(Subject.id == topic.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db_topic = Topic(subject_id=topic.subject_id, name=topic.name, description=topic.description)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.get("/topics")
def get_topics(subject_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get all topics"""
    query = db.query(Topic)
    if subject_id:
        query = query.filter(Topic.subject_id == subject_id)
    return query.all()

@router.post("/questions")
def create_question(question: QuestionCreate, admin_password: str = Query(...), db: Session = Depends(get_db)):
    """Create a new question"""
    verify_admin(admin_password)
    
    # Verify topic, subject, and exam exist
    topic = db.query(Topic).filter(Topic.id == question.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db_question = Question(
        exam_id=question.exam_id,
        subject_id=question.subject_id,
        topic_id=question.topic_id,
        question_text=question.question_text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        difficulty_level=question.difficulty_level
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.put("/questions/{question_id}")
def update_question(
    question_id: int,
    question: QuestionCreate,
    admin_password: str = Query(...),
    db: Session = Depends(get_db)
):
    """Update a question"""
    verify_admin(admin_password)
    
    # Verify question exists
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_question.exam_id = question.exam_id
    db_question.subject_id = question.subject_id
    db_question.topic_id = question.topic_id
    db_question.question_text = question.question_text
    db_question.option_a = question.option_a
    db_question.option_b = question.option_b
    db_question.option_c = question.option_c
    db_question.option_d = question.option_d
    db_question.correct_answer = question.correct_answer
    db_question.explanation = question.explanation
    db_question.difficulty_level = question.difficulty_level
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    admin_password: str = Query(...),
    db: Session = Depends(get_db)
):
    """Delete a question"""
    verify_admin(admin_password)
    
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(db_question)
    db.commit()
    
    return {"message": "Question deleted successfully"}

@router.get("/statistics")
def get_statistics(admin_password: str = Query(...), db: Session = Depends(get_db)):
    """Get platform statistics"""
    verify_admin(admin_password)
    
    users_count = db.query(func.count(User.id)).scalar()
    questions_count = db.query(func.count(Question.id)).scalar()
    attempts_count = db.query(func.count(UserProgress.id)).scalar()
    
    return {
        "total_users": users_count,
        "total_questions": questions_count,
        "total_attempts": attempts_count
    }

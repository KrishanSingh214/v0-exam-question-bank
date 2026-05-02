from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import List, Optional
import os
import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import logging

load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/question_bank"
)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(
    title="Question Bank API",
    description="ML-powered question bank for exam preparation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Database Models ====================

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    full_name = Column(String(255))
    target_exam = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExamDB(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    description = Column(Text)
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class SubjectDB(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    name = Column(String(100), index=True)
    description = Column(Text)

class TopicDB(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    name = Column(String(100), index=True)
    description = Column(Text)

class QuestionDB(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    question_text = Column(Text)
    question_type = Column(String(50))
    difficulty_level = Column(String(20))
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class OptionDB(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_text = Column(Text)
    option_label = Column(String(10))
    is_correct = Column(Boolean, default=False)

class UserProgressDB(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    answer_selected = Column(String(500))
    is_correct = Column(Boolean)
    attempts = Column(Integer, default=1)
    last_attempted = Column(DateTime, default=datetime.utcnow)
    time_spent_seconds = Column(Integer)

class BookmarkDB(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class WeakTopicDB(Base):
    __tablename__ = "weak_topics"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    accuracy_percentage = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)

class QuizSessionDB(Base):
    __tablename__ = "quiz_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    score = Column(Float)
    duration_seconds = Column(Integer)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

# Create tables
Base.metadata.create_all(bind=engine)

# ==================== Pydantic Models ====================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    target_exam: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    target_exam: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    difficulty_level: str
    question_type: str

class OptionResponse(BaseModel):
    id: int
    option_text: str
    option_label: str

class QuestionDetailResponse(BaseModel):
    id: int
    question_text: str
    difficulty_level: str
    question_type: str
    explanation: str
    options: List[OptionResponse]

# ==================== Utility Functions ====================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ==================== Auth Routes ====================

@app.post("/api/auth/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(UserDB).filter(
        (UserDB.email == user_data.email) | (UserDB.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new user
    new_user = UserDB(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        target_exam=user_data.target_exam
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create token
    access_token = create_access_token(
        data={"sub": new_user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**{
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "target_exam": new_user.target_exam
        })
    }

@app.post("/api/auth/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "target_exam": user.target_exam
        })
    }

# ==================== Question Routes ====================

@app.get("/api/questions", response_model=List[QuestionResponse])
def get_questions(
    exam_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    topic_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(QuestionDB)
    
    if topic_id:
        query = query.filter(QuestionDB.topic_id == topic_id)
    if difficulty:
        query = query.filter(QuestionDB.difficulty_level == difficulty)
    
    questions = query.offset(skip).limit(limit).all()
    return questions

@app.get("/api/questions/{question_id}", response_model=QuestionDetailResponse)
def get_question_detail(question_id: int, db: Session = Depends(get_db)):
    question = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    options = db.query(OptionDB).filter(OptionDB.question_id == question_id).all()
    
    return {
        "id": question.id,
        "question_text": question.question_text,
        "difficulty_level": question.difficulty_level,
        "question_type": question.question_type,
        "explanation": question.explanation or "",
        "options": [{"id": o.id, "option_text": o.option_text, "option_label": o.option_label} for o in options]
    }

# ==================== Exam Routes ====================

@app.get("/api/exams")
def get_exams(db: Session = Depends(get_db)):
    exams = db.query(ExamDB).all()
    return exams

@app.get("/api/exams/{exam_id}/subjects")
def get_exam_subjects(exam_id: int, db: Session = Depends(get_db)):
    subjects = db.query(SubjectDB).filter(SubjectDB.exam_id == exam_id).all()
    return subjects

@app.get("/api/subjects/{subject_id}/topics")
def get_subject_topics(subject_id: int, db: Session = Depends(get_db)):
    topics = db.query(TopicDB).filter(TopicDB.subject_id == subject_id).all()
    return topics

# ==================== User Progress Routes ====================

@app.post("/api/progress/submit")
def submit_answer(
    question_id: int,
    answer: str,
    time_spent: int,
    credentials: HTTPAuthCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    user_id = token_data["user_id"]
    
    # Get question and check answer
    question = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    correct_option = db.query(OptionDB).filter(
        (OptionDB.question_id == question_id) & (OptionDB.is_correct == True)
    ).first()
    
    is_correct = correct_option.option_label == answer if correct_option else False
    
    # Update or create progress
    progress = db.query(UserProgressDB).filter(
        (UserProgressDB.user_id == user_id) & (UserProgressDB.question_id == question_id)
    ).first()
    
    if progress:
        progress.attempts += 1
        progress.is_correct = is_correct
        progress.answer_selected = answer
        progress.last_attempted = datetime.utcnow()
        progress.time_spent_seconds = (progress.time_spent_seconds or 0) + time_spent
    else:
        progress = UserProgressDB(
            user_id=user_id,
            question_id=question_id,
            exam_id=question.topic_id,
            answer_selected=answer,
            is_correct=is_correct,
            time_spent_seconds=time_spent
        )
        db.add(progress)
    
    db.commit()
    return {"is_correct": is_correct, "message": "Answer submitted successfully"}

@app.get("/api/progress/user")
def get_user_progress(
    credentials: HTTPAuthCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    user_id = token_data["user_id"]
    
    progress = db.query(UserProgressDB).filter(UserProgressDB.user_id == user_id).all()
    
    total_questions = len(progress)
    correct_answers = sum(1 for p in progress if p.is_correct)
    accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    return {
        "total_questions_attempted": total_questions,
        "correct_answers": correct_answers,
        "accuracy_percentage": accuracy
    }

# ==================== Recommendations Routes ====================

@app.get("/api/recommendations")
def get_recommendations(
    limit: int = 10,
    credentials: HTTPAuthCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    user_id = token_data["user_id"]
    
    # Get weak topics
    weak_topics = db.query(WeakTopicDB).filter(
        WeakTopicDB.user_id == user_id
    ).order_by(WeakTopicDB.accuracy_percentage).limit(5).all()
    
    recommended_questions = []
    for weak_topic in weak_topics:
        questions = db.query(QuestionDB).filter(
            QuestionDB.topic_id == weak_topic.topic_id
        ).limit(limit // len(weak_topics) if weak_topics else limit).all()
        recommended_questions.extend(questions)
    
    return recommended_questions[:limit]

# ==================== Bookmarks Routes ====================

@app.post("/api/bookmarks/{question_id}")
def add_bookmark(
    question_id: int,
    credentials: HTTPAuthCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    user_id = token_data["user_id"]
    
    bookmark = BookmarkDB(user_id=user_id, question_id=question_id)
    db.add(bookmark)
    db.commit()
    return {"message": "Bookmarked successfully"}

@app.delete("/api/bookmarks/{question_id}")
def remove_bookmark(
    question_id: int,
    credentials: HTTPAuthCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    user_id = token_data["user_id"]
    
    bookmark = db.query(BookmarkDB).filter(
        (BookmarkDB.user_id == user_id) & (BookmarkDB.question_id == question_id)
    ).first()
    
    if bookmark:
        db.delete(bookmark)
        db.commit()
    
    return {"message": "Bookmark removed"}

@app.get("/api/bookmarks")
def get_bookmarks(
    credentials: HTTPAuthCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    user_id = token_data["user_id"]
    
    bookmarks = db.query(BookmarkDB).filter(BookmarkDB.user_id == user_id).all()
    question_ids = [b.question_id for b in bookmarks]
    questions = db.query(QuestionDB).filter(QuestionDB.id.in_(question_ids)).all()
    
    return questions

# ==================== Health Check ====================

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Question Bank API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

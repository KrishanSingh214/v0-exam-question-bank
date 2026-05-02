from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    target_exam: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    target_exam: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Question Schemas
class OptionResponse(BaseModel):
    id: int
    option_text: str
    is_correct: Optional[bool] = None

class OptionCreate(BaseModel):
    option_text: str
    is_correct: bool

class QuestionCreate(BaseModel):
    topic_id: int
    subject_id: int
    exam_id: int
    question_text: str
    question_type: str
    difficulty_level: str
    options: Optional[List[OptionCreate]] = []

class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    subject_id: int
    exam_id: int
    question_text: str
    question_type: str
    difficulty_level: str
    created_at: datetime
    options: Optional[List[OptionResponse]] = []

class QuestionWithProgressResponse(QuestionResponse):
    is_attempted: bool
    is_correct: Optional[bool] = None
    is_bookmarked: bool

# Exam Schemas
class ExamCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ExamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Subject Schemas
class SubjectCreate(BaseModel):
    name: str
    exam_id: int
    description: Optional[str] = None

class SubjectResponse(BaseModel):
    id: int
    name: str
    exam_id: int
    description: Optional[str] = None

# Topic Schemas
class TopicCreate(BaseModel):
    name: str
    subject_id: int
    description: Optional[str] = None

class TopicResponse(BaseModel):
    id: int
    name: str
    subject_id: int
    description: Optional[str] = None

# Progress Schemas
class UserProgressCreate(BaseModel):
    question_id: int
    is_correct: bool
    time_spent_seconds: Optional[int] = None

class UserProgressResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    is_correct: bool
    attempted_at: datetime
    time_spent_seconds: Optional[int] = None

# Recommendation Schemas
class RecommendationResponse(BaseModel):
    question_id: int
    reason: str
    weak_topic: str
    question_text: str
    difficulty_level: str

class UserStatsResponse(BaseModel):
    total_attempted: int
    total_correct: int
    accuracy_percentage: float
    weak_topics: List[dict]

# Bookmark Schemas
class BookmarkCreate(BaseModel):
    question_id: int

class BookmarkResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    created_at: datetime

# Search Schemas
class QuestionSearchRequest(BaseModel):
    exam_id: Optional[int] = None
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    difficulty_level: Optional[str] = None
    question_type: Optional[str] = None
    keyword: Optional[str] = None
    limit: int = 20
    offset: int = 0

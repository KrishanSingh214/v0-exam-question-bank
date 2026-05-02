from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas import QuestionCreate, ExamCreate, SubjectCreate, TopicCreate, QuestionResponse, ExamResponse, SubjectResponse, TopicResponse
from database import get_db

router = APIRouter()

# Admin password for simple auth
ADMIN_PASSWORD = "admin123"  # Change this in production

def verify_admin(admin_password: str):
    """Simple admin verification"""
    if admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/exams", response_model=ExamResponse)
def create_exam(exam: ExamCreate, admin_password: str, db = Depends(get_db)):
    """Create a new exam"""
    verify_admin(admin_password)
    
    db.connect()
    
    # Check if exam already exists
    query = "SELECT id FROM exams WHERE name = %s"
    existing = db.execute_single(query, (exam.name,))
    if existing:
        db.disconnect()
        raise HTTPException(status_code=400, detail="Exam already exists")
    
    # Create exam
    query = "INSERT INTO exams (name, description) VALUES (%s, %s) RETURNING id, name, description"
    result = db.execute_single(query, (exam.name, exam.description))
    db.disconnect()
    
    return ExamResponse(**dict(result))

@router.get("/exams", response_model=List[ExamResponse])
def get_exams(db = Depends(get_db)):
    """Get all exams"""
    db.connect()
    query = "SELECT id, name, description FROM exams"
    exams = db.execute_query(query)
    db.disconnect()
    return [ExamResponse(**dict(e)) for e in exams]

@router.post("/subjects", response_model=SubjectResponse)
def create_subject(subject: SubjectCreate, admin_password: str, db = Depends(get_db)):
    """Create a new subject"""
    verify_admin(admin_password)
    
    db.connect()
    
    # Verify exam exists
    query = "SELECT id FROM exams WHERE id = %s"
    exam = db.execute_single(query, (subject.exam_id,))
    if not exam:
        db.disconnect()
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Create subject
    query = "INSERT INTO subjects (name, exam_id, description) VALUES (%s, %s, %s) RETURNING id, name, exam_id, description"
    result = db.execute_single(query, (subject.name, subject.exam_id, subject.description))
    db.disconnect()
    
    return SubjectResponse(**dict(result))

@router.get("/subjects", response_model=List[SubjectResponse])
def get_subjects(exam_id: int = None, db = Depends(get_db)):
    """Get all subjects"""
    db.connect()
    
    if exam_id:
        query = "SELECT id, name, exam_id, description FROM subjects WHERE exam_id = %s"
        subjects = db.execute_query(query, (exam_id,))
    else:
        query = "SELECT id, name, exam_id, description FROM subjects"
        subjects = db.execute_query(query)
    
    db.disconnect()
    return [SubjectResponse(**dict(s)) for s in subjects]

@router.post("/topics", response_model=TopicResponse)
def create_topic(topic: TopicCreate, admin_password: str, db = Depends(get_db)):
    """Create a new topic"""
    verify_admin(admin_password)
    
    db.connect()
    
    # Verify subject exists
    query = "SELECT id FROM subjects WHERE id = %s"
    subject = db.execute_single(query, (topic.subject_id,))
    if not subject:
        db.disconnect()
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Create topic
    query = "INSERT INTO topics (name, subject_id, description) VALUES (%s, %s, %s) RETURNING id, name, subject_id, description"
    result = db.execute_single(query, (topic.name, topic.subject_id, topic.description))
    db.disconnect()
    
    return TopicResponse(**dict(result))

@router.get("/topics", response_model=List[TopicResponse])
def get_topics(subject_id: int = None, db = Depends(get_db)):
    """Get all topics"""
    db.connect()
    
    if subject_id:
        query = "SELECT id, name, subject_id, description FROM topics WHERE subject_id = %s"
        topics = db.execute_query(query, (subject_id,))
    else:
        query = "SELECT id, name, subject_id, description FROM topics"
        topics = db.execute_query(query)
    
    db.disconnect()
    return [TopicResponse(**dict(t)) for t in topics]

@router.post("/questions", response_model=QuestionResponse)
def create_question(question: QuestionCreate, admin_password: str, db = Depends(get_db)):
    """Create a new question"""
    verify_admin(admin_password)
    
    db.connect()
    
    # Verify topic, subject, and exam exist
    verify_query = "SELECT id FROM topics WHERE id = %s"
    if not db.execute_single(verify_query, (question.topic_id,)):
        db.disconnect()
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Create question
    query = """
    INSERT INTO questions (topic_id, subject_id, exam_id, question_text, question_type, difficulty_level)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id, topic_id, subject_id, exam_id, question_text, question_type, difficulty_level, created_at
    """
    params = (
        question.topic_id,
        question.subject_id,
        question.exam_id,
        question.question_text,
        question.question_type,
        question.difficulty_level
    )
    result = db.execute_single(query, params)
    question_id = result['id']
    
    # Add options if MCQ
    if question.options:
        for option in question.options:
            option_query = "INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)"
            db.execute_insert(option_query, (question_id, option.option_text, option.is_correct))
    
    db.disconnect()
    
    return QuestionResponse(**dict(result))

@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int, question: QuestionCreate, admin_password: str, db = Depends(get_db)):
    """Update a question"""
    verify_admin(admin_password)
    
    db.connect()
    
    # Verify question exists
    query = "SELECT id FROM questions WHERE id = %s"
    if not db.execute_single(query, (question_id,)):
        db.disconnect()
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Update question
    query = """
    UPDATE questions
    SET topic_id = %s, subject_id = %s, exam_id = %s, question_text = %s, question_type = %s, difficulty_level = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s
    RETURNING id, topic_id, subject_id, exam_id, question_text, question_type, difficulty_level, created_at
    """
    params = (
        question.topic_id,
        question.subject_id,
        question.exam_id,
        question.question_text,
        question.question_type,
        question.difficulty_level,
        question_id
    )
    result = db.execute_single(query, params)
    
    # Update options if provided
    if question.options:
        # Delete existing options
        delete_query = "DELETE FROM options WHERE question_id = %s"
        db.execute_update(delete_query, (question_id,))
        
        # Add new options
        for option in question.options:
            option_query = "INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)"
            db.execute_insert(option_query, (question_id, option.option_text, option.is_correct))
    
    db.disconnect()
    
    return QuestionResponse(**dict(result))

@router.delete("/questions/{question_id}")
def delete_question(question_id: int, admin_password: str, db = Depends(get_db)):
    """Delete a question"""
    verify_admin(admin_password)
    
    db.connect()
    
    # Delete question (cascades to options and user_progress)
    query = "DELETE FROM questions WHERE id = %s"
    db.execute_update(query, (question_id,))
    db.disconnect()
    
    return {"message": "Question deleted successfully"}

@router.get("/statistics")
def get_statistics(admin_password: str, db = Depends(get_db)):
    """Get platform statistics"""
    verify_admin(admin_password)
    
    db.connect()
    
    # Get counts
    users_query = "SELECT COUNT(*) as count FROM users"
    questions_query = "SELECT COUNT(*) as count FROM questions"
    attempts_query = "SELECT COUNT(*) as count FROM user_progress"
    
    users = db.execute_single(users_query)
    questions = db.execute_single(questions_query)
    attempts = db.execute_single(attempts_query)
    
    db.disconnect()
    
    return {
        "total_users": users['count'],
        "total_questions": questions['count'],
        "total_attempts": attempts['count']
    }

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from schemas import QuestionResponse, QuestionSearchRequest, BookmarkCreate, BookmarkResponse, UserProgressCreate
from database import get_db
from utils import extract_user_id_from_token

router = APIRouter()

@router.get("/", response_model=List[QuestionResponse])
def get_questions(
    exam_id: int = Query(None),
    subject_id: int = Query(None),
    topic_id: int = Query(None),
    difficulty_level: str = Query(None),
    question_type: str = Query(None),
    keyword: str = Query(None),
    limit: int = Query(20),
    offset: int = Query(0),
    db = Depends(get_db)
):
    """Get questions with filters"""
    db.connect()
    
    query = "SELECT id, topic_id, subject_id, exam_id, question_text, question_type, difficulty_level, created_at FROM questions WHERE 1=1"
    params = []
    
    if exam_id:
        query += " AND exam_id = %s"
        params.append(exam_id)
    if subject_id:
        query += " AND subject_id = %s"
        params.append(subject_id)
    if topic_id:
        query += " AND topic_id = %s"
        params.append(topic_id)
    if difficulty_level:
        query += " AND difficulty_level = %s"
        params.append(difficulty_level)
    if question_type:
        query += " AND question_type = %s"
        params.append(question_type)
    if keyword:
        query += " AND question_text ILIKE %s"
        params.append(f"%{keyword}%")
    
    query += f" LIMIT {limit} OFFSET {offset}"
    
    questions = db.execute_query(query, params if params else None)
    db.disconnect()
    
    return [QuestionResponse(**dict(q)) for q in questions]

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db = Depends(get_db)):
    """Get a single question with options"""
    db.connect()
    
    query = """
    SELECT id, topic_id, subject_id, exam_id, question_text, question_type, difficulty_level, created_at
    FROM questions WHERE id = %s
    """
    question = db.execute_single(query, (question_id,))
    
    if not question:
        db.disconnect()
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Get options
    options_query = "SELECT id, option_text, is_correct FROM options WHERE question_id = %s"
    options = db.execute_query(options_query, (question_id,))
    db.disconnect()
    
    question_dict = dict(question)
    question_dict['options'] = [dict(o) for o in options]
    
    return QuestionResponse(**question_dict)

@router.get("/search/advanced", response_model=List[QuestionResponse])
def search_questions(search: QuestionSearchRequest = Depends(), db = Depends(get_db)):
    """Advanced question search"""
    db.connect()
    
    query = "SELECT id, topic_id, subject_id, exam_id, question_text, question_type, difficulty_level, created_at FROM questions WHERE 1=1"
    params = []
    
    if search.exam_id:
        query += " AND exam_id = %s"
        params.append(search.exam_id)
    if search.subject_id:
        query += " AND subject_id = %s"
        params.append(search.subject_id)
    if search.topic_id:
        query += " AND topic_id = %s"
        params.append(search.topic_id)
    if search.difficulty_level:
        query += " AND difficulty_level = %s"
        params.append(search.difficulty_level)
    if search.question_type:
        query += " AND question_type = %s"
        params.append(search.question_type)
    if search.keyword:
        query += " AND question_text ILIKE %s"
        params.append(f"%{search.keyword}%")
    
    query += f" LIMIT {search.limit} OFFSET {search.offset}"
    
    questions = db.execute_query(query, params if params else None)
    db.disconnect()
    
    return [QuestionResponse(**dict(q)) for q in questions]

@router.post("/bookmarks", response_model=BookmarkResponse)
def add_bookmark(bookmark: BookmarkCreate, authorization: str = None, db = Depends(get_db)):
    """Add question to bookmarks"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    # Check if question exists
    query = "SELECT id FROM questions WHERE id = %s"
    question = db.execute_single(query, (bookmark.question_id,))
    if not question:
        db.disconnect()
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Add bookmark
    query = """
    INSERT INTO bookmarks (user_id, question_id)
    VALUES (%s, %s)
    ON CONFLICT (user_id, question_id) DO NOTHING
    RETURNING id, user_id, question_id, created_at
    """
    result = db.execute_single(query, (user_id, bookmark.question_id))
    db.disconnect()
    
    if result:
        return BookmarkResponse(**dict(result))
    raise HTTPException(status_code=400, detail="Failed to add bookmark")

@router.get("/bookmarks/user", response_model=List[QuestionResponse])
def get_bookmarks(authorization: str = None, db = Depends(get_db)):
    """Get user's bookmarked questions"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    query = """
    SELECT q.id, q.topic_id, q.subject_id, q.exam_id, q.question_text, q.question_type, q.difficulty_level, q.created_at
    FROM questions q
    INNER JOIN bookmarks b ON q.id = b.question_id
    WHERE b.user_id = %s
    """
    questions = db.execute_query(query, (user_id,))
    db.disconnect()
    
    return [QuestionResponse(**dict(q)) for q in questions]

@router.delete("/bookmarks/{question_id}")
def remove_bookmark(question_id: int, authorization: str = None, db = Depends(get_db)):
    """Remove question from bookmarks"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    query = "DELETE FROM bookmarks WHERE user_id = %s AND question_id = %s"
    db.execute_update(query, (user_id, question_id))
    db.disconnect()
    
    return {"message": "Bookmark removed"}

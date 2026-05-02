from fastapi import APIRouter, HTTPException, Depends
from schemas import UserProgressCreate, UserProgressResponse, UserStatsResponse
from database import get_db
from utils import extract_user_id_from_token

router = APIRouter()

@router.post("/progress", response_model=UserProgressResponse)
def record_progress(progress: UserProgressCreate, authorization: str = None, db = Depends(get_db)):
    """Record user progress on a question"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    # Check if question exists
    query = "SELECT id FROM questions WHERE id = %s"
    question = db.execute_single(query, (progress.question_id,))
    if not question:
        db.disconnect()
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Insert or update progress
    query = """
    INSERT INTO user_progress (user_id, question_id, is_correct, time_spent_seconds)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (user_id, question_id) DO UPDATE
    SET is_correct = EXCLUDED.is_correct, time_spent_seconds = EXCLUDED.time_spent_seconds, attempted_at = CURRENT_TIMESTAMP
    RETURNING id, user_id, question_id, is_correct, attempted_at, time_spent_seconds
    """
    params = (user_id, progress.question_id, progress.is_correct, progress.time_spent_seconds)
    result = db.execute_single(query, params)
    db.disconnect()
    
    if result:
        return UserProgressResponse(**dict(result))
    raise HTTPException(status_code=400, detail="Failed to record progress")

@router.get("/stats", response_model=UserStatsResponse)
def get_user_stats(authorization: str = None, db = Depends(get_db)):
    """Get user statistics and weak topics"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    # Get overall stats
    stats_query = """
    SELECT 
        COUNT(*) as total_attempted,
        SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as total_correct
    FROM user_progress WHERE user_id = %s
    """
    stats = db.execute_single(stats_query, (user_id,))
    
    total_attempted = stats['total_attempted'] or 0
    total_correct = stats['total_correct'] or 0
    accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
    
    # Get weak topics (topics with less than 60% accuracy)
    weak_topics_query = """
    SELECT 
        t.id,
        t.name,
        COUNT(up.id) as attempted,
        SUM(CASE WHEN up.is_correct THEN 1 ELSE 0 END) as correct,
        ROUND(SUM(CASE WHEN up.is_correct THEN 1 ELSE 0 END)::numeric / COUNT(up.id) * 100, 2) as accuracy
    FROM topics t
    LEFT JOIN questions q ON t.id = q.topic_id
    LEFT JOIN user_progress up ON q.id = up.question_id AND up.user_id = %s
    WHERE up.id IS NOT NULL
    GROUP BY t.id, t.name
    HAVING ROUND(SUM(CASE WHEN up.is_correct THEN 1 ELSE 0 END)::numeric / COUNT(up.id) * 100, 2) < 60
    ORDER BY accuracy ASC
    """
    weak_topics = db.execute_query(weak_topics_query, (user_id,))
    
    db.disconnect()
    
    weak_topics_list = [
        {
            "topic_id": wt['id'],
            "topic_name": wt['name'],
            "attempted": wt['attempted'],
            "correct": wt['correct'],
            "accuracy_percentage": float(wt['accuracy'])
        }
        for wt in weak_topics
    ]
    
    return UserStatsResponse(
        total_attempted=total_attempted,
        total_correct=total_correct,
        accuracy_percentage=accuracy,
        weak_topics=weak_topics_list
    )

@router.get("/progress/{question_id}")
def get_question_progress(question_id: int, authorization: str = None, db = Depends(get_db)):
    """Get user's progress on a specific question"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    query = """
    SELECT id, user_id, question_id, is_correct, attempted_at, time_spent_seconds
    FROM user_progress
    WHERE user_id = %s AND question_id = %s
    """
    progress = db.execute_single(query, (user_id, question_id))
    db.disconnect()
    
    if not progress:
        return {"attempted": False}
    
    return {
        "attempted": True,
        "is_correct": progress['is_correct'],
        "time_spent_seconds": progress['time_spent_seconds'],
        "attempted_at": progress['attempted_at']
    }

@router.get("/history")
def get_attempt_history(authorization: str = None, limit: int = 50, offset: int = 0, db = Depends(get_db)):
    """Get user's question attempt history"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    query = """
    SELECT 
        up.id,
        up.question_id,
        q.question_text,
        q.difficulty_level,
        up.is_correct,
        up.attempted_at,
        up.time_spent_seconds
    FROM user_progress up
    JOIN questions q ON up.question_id = q.id
    WHERE up.user_id = %s
    ORDER BY up.attempted_at DESC
    LIMIT %s OFFSET %s
    """
    history = db.execute_query(query, (user_id, limit, offset))
    db.disconnect()
    
    return [dict(h) for h in history]

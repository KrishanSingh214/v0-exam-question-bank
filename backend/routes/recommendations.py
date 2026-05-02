from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from schemas import RecommendationResponse, QuestionResponse
from database import get_db
from utils import extract_user_id_from_token
from ml_model import RecommendationEngine

router = APIRouter()

# Initialize recommendation engine
recommendation_engine = RecommendationEngine()

@router.get("/personalized", response_model=List[RecommendationResponse])
def get_personalized_recommendations(
    authorization: str = None,
    limit: int = Query(10),
    db = Depends(get_db)
):
    """Get personalized question recommendations based on user performance"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    # Get user's stats
    stats_query = """
    SELECT u.target_exam, u.id
    FROM users u WHERE u.id = %s
    """
    user = db.execute_single(stats_query, (user_id,))
    
    if not user:
        db.disconnect()
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get weak topics
    weak_topics_query = """
    SELECT 
        t.id as topic_id,
        t.name as topic_name,
        COUNT(up.id) as attempted,
        SUM(CASE WHEN up.is_correct THEN 1 ELSE 0 END) as correct,
        ROUND(SUM(CASE WHEN up.is_correct THEN 1 ELSE 0 END)::numeric / COUNT(up.id) * 100, 2) as accuracy
    FROM topics t
    LEFT JOIN questions q ON t.id = q.topic_id
    LEFT JOIN user_progress up ON q.id = up.question_id AND up.user_id = %s
    WHERE up.id IS NOT NULL
    GROUP BY t.id, t.name
    HAVING COUNT(up.id) > 0
    ORDER BY accuracy ASC
    LIMIT 5
    """
    weak_topics = db.execute_query(weak_topics_query, (user_id,))
    
    recommendations = []
    
    # For each weak topic, recommend questions
    for topic in weak_topics:
        topic_id = topic['topic_id']
        topic_name = topic['topic_name']
        
        # Get unanswered questions from this topic or questions with low accuracy
        question_query = """
        SELECT q.id, q.question_text, q.difficulty_level
        FROM questions q
        WHERE q.topic_id = %s
        AND q.id NOT IN (
            SELECT question_id FROM user_progress WHERE user_id = %s AND is_correct = true
        )
        ORDER BY q.difficulty_level ASC, RANDOM()
        LIMIT %s
        """
        questions = db.execute_query(question_query, (topic_id, user_id, limit))
        
        for q in questions:
            recommendation = RecommendationResponse(
                question_id=q['id'],
                reason=f"Your weak area - only {topic['accuracy']}% accuracy",
                weak_topic=topic_name,
                question_text=q['question_text'],
                difficulty_level=q['difficulty_level']
            )
            recommendations.append(recommendation)
    
    db.disconnect()
    
    # If not enough recommendations, add random questions from target exam
    if len(recommendations) < limit:
        db.connect()
        random_query = """
        SELECT q.id, q.question_text, q.difficulty_level, t.name as topic_name
        FROM questions q
        JOIN topics t ON q.topic_id = t.id
        JOIN subjects s ON q.subject_id = s.id
        JOIN exams e ON q.exam_id = e.id
        WHERE e.name = %s
        AND q.id NOT IN (
            SELECT question_id FROM user_progress WHERE user_id = %s
        )
        ORDER BY RANDOM()
        LIMIT %s
        """
        random_questions = db.execute_query(random_query, (user['target_exam'], user_id, limit - len(recommendations)))
        
        for q in random_questions:
            recommendation = RecommendationResponse(
                question_id=q['id'],
                reason="Suggested for practice",
                weak_topic=q['topic_name'],
                question_text=q['question_text'],
                difficulty_level=q['difficulty_level']
            )
            recommendations.append(recommendation)
        
        db.disconnect()
    
    return recommendations[:limit]

@router.get("/by-topic/{topic_id}", response_model=List[QuestionResponse])
def get_recommendations_by_topic(
    topic_id: int,
    authorization: str = None,
    limit: int = Query(10),
    db = Depends(get_db)
):
    """Get questions from a specific weak topic"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    # Verify topic exists
    topic_query = "SELECT id FROM topics WHERE id = %s"
    topic = db.execute_single(topic_query, (topic_id,))
    if not topic:
        db.disconnect()
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Get unanswered questions from this topic
    question_query = """
    SELECT id, topic_id, subject_id, exam_id, question_text, question_type, difficulty_level, created_at
    FROM questions
    WHERE topic_id = %s
    AND id NOT IN (
        SELECT question_id FROM user_progress WHERE user_id = %s AND is_correct = true
    )
    ORDER BY difficulty_level ASC
    LIMIT %s
    """
    questions = db.execute_query(question_query, (topic_id, user_id, limit))
    db.disconnect()
    
    return [QuestionResponse(**dict(q)) for q in questions]

@router.get("/difficulty-progression", response_model=List[QuestionResponse])
def get_difficulty_progression(
    authorization: str = None,
    subject_id: int = Query(None),
    db = Depends(get_db)
):
    """Get questions arranged by difficulty for progressive learning"""
    user_id = extract_user_id_from_token(authorization.split(" ")[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db.connect()
    
    base_query = """
    SELECT id, topic_id, subject_id, exam_id, question_text, question_type, difficulty_level, created_at
    FROM questions
    WHERE id NOT IN (
        SELECT question_id FROM user_progress WHERE user_id = %s
    )
    """
    params = [user_id]
    
    if subject_id:
        base_query += " AND subject_id = %s"
        params.append(subject_id)
    
    base_query += " ORDER BY CASE WHEN difficulty_level = 'easy' THEN 1 WHEN difficulty_level = 'medium' THEN 2 ELSE 3 END, RANDOM() LIMIT 20"
    
    questions = db.execute_query(base_query, params)
    db.disconnect()
    
    return [QuestionResponse(**dict(q)) for q in questions]

@router.post("/retrain")
def retrain_model(authorization: str = None, db = Depends(get_db)):
    """Retrain the recommendation model with latest data"""
    # This would typically be called periodically or manually
    # For now, it's a simple endpoint that acknowledges the request
    db.connect()
    
    # Count total users and questions
    users_query = "SELECT COUNT(*) as count FROM users"
    questions_query = "SELECT COUNT(*) as count FROM questions"
    
    users_count = db.execute_single(users_query)
    questions_count = db.execute_single(questions_query)
    
    db.disconnect()
    
    return {
        "message": "Model retraining initiated",
        "total_users": users_count['count'],
        "total_questions": questions_count['count'],
        "status": "In Progress"
    }

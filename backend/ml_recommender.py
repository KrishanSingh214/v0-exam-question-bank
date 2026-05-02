import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    ML-powered recommendation engine using collaborative filtering and content-based features.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.scaler = StandardScaler()
    
    def calculate_topic_accuracy(self, user_id: int, topic_id: int) -> float:
        """Calculate user's accuracy percentage for a specific topic."""
        from app import UserProgressDB, QuestionDB
        
        attempts = self.db.query(UserProgressDB).join(
            QuestionDB, UserProgressDB.question_id == QuestionDB.id
        ).filter(
            (UserProgressDB.user_id == user_id) & (QuestionDB.topic_id == topic_id)
        ).all()
        
        if not attempts:
            return 50.0  # Default accuracy for untested topics
        
        correct = sum(1 for a in attempts if a.is_correct)
        return (correct / len(attempts)) * 100
    
    def identify_weak_topics(self, user_id: int, threshold: float = 70.0) -> List[Tuple[int, float]]:
        """Identify topics where user's accuracy is below threshold."""
        from app import TopicDB
        
        topics = self.db.query(TopicDB).all()
        weak_topics = []
        
        for topic in topics:
            accuracy = self.calculate_topic_accuracy(user_id, topic.id)
            if accuracy < threshold:
                weak_topics.append((topic.id, accuracy))
        
        # Sort by lowest accuracy first
        weak_topics.sort(key=lambda x: x[1])
        return weak_topics
    
    def get_personalized_recommendations(self, user_id: int, limit: int = 10) -> List[int]:
        """
        Generate personalized question recommendations based on:
        1. Weak topic areas (low accuracy)
        2. Difficulty level progression
        3. Question variety
        """
        from app import UserProgressDB, QuestionDB, WeakTopicDB
        
        # Get weak topics
        weak_topics = self.identify_weak_topics(user_id, threshold=70.0)
        
        if not weak_topics:
            # If no weak topics, recommend high-difficulty questions for practice
            return self._get_difficulty_based_recommendations(user_id, limit)
        
        # Update weak topics in database
        for topic_id, accuracy in weak_topics[:5]:
            weak_topic = self.db.query(WeakTopicDB).filter(
                (WeakTopicDB.user_id == user_id) & (WeakTopicDB.topic_id == topic_id)
            ).first()
            
            if weak_topic:
                weak_topic.accuracy_percentage = accuracy
            else:
                weak_topic = WeakTopicDB(
                    user_id=user_id,
                    topic_id=topic_id,
                    accuracy_percentage=accuracy
                )
                self.db.add(weak_topic)
        
        self.db.commit()
        
        # Get unanswered questions from weak topics
        attempted_questions = self.db.query(UserProgressDB.question_id).filter(
            UserProgressDB.user_id == user_id
        ).all()
        attempted_ids = [q[0] for q in attempted_questions]
        
        weak_topic_ids = [t[0] for t in weak_topics[:5]]
        
        recommendations = self.db.query(QuestionDB).filter(
            (QuestionDB.topic_id.in_(weak_topic_ids)) &
            (~QuestionDB.id.in_(attempted_ids))
        ).order_by(
            QuestionDB.difficulty_level.desc(),
            QuestionDB.id
        ).limit(limit).all()
        
        return [q.id for q in recommendations]
    
    def _get_difficulty_based_recommendations(self, user_id: int, limit: int = 10) -> List[int]:
        """Get recommendations based on difficulty progression when user has no weak topics."""
        from app import UserProgressDB, QuestionDB
        
        # Get user's average accuracy across all attempted questions
        attempts = self.db.query(UserProgressDB).filter(
            UserProgressDB.user_id == user_id
        ).all()
        
        if not attempts:
            # New user - recommend easy questions
            return [q.id for q in self.db.query(QuestionDB).filter(
                QuestionDB.difficulty_level == "Easy"
            ).limit(limit).all()]
        
        accuracy = sum(1 for a in attempts if a.is_correct) / len(attempts)
        
        # Choose difficulty based on accuracy
        if accuracy < 0.5:
            difficulty = "Easy"
        elif accuracy < 0.75:
            difficulty = "Medium"
        else:
            difficulty = "Hard"
        
        attempted_ids = [a.question_id for a in attempts]
        
        recommendations = self.db.query(QuestionDB).filter(
            (QuestionDB.difficulty_level == difficulty) &
            (~QuestionDB.id.in_(attempted_ids))
        ).limit(limit).all()
        
        return [q.id for q in recommendations]
    
    def content_similarity_recommendations(self, question_id: int, limit: int = 5) -> List[int]:
        """Find similar questions based on content features."""
        from app import QuestionDB, OptionDB
        
        target_question = self.db.query(QuestionDB).filter(
            QuestionDB.id == question_id
        ).first()
        
        if not target_question:
            return []
        
        # Get all questions from same topic
        similar_questions = self.db.query(QuestionDB).filter(
            (QuestionDB.topic_id == target_question.topic_id) &
            (QuestionDB.id != question_id) &
            (QuestionDB.difficulty_level == target_question.difficulty_level)
        ).limit(limit).all()
        
        return [q.id for q in similar_questions]
    
    def get_trending_topics(self, limit: int = 5) -> List[dict]:
        """Get most attempted topics across all users."""
        from app import UserProgressDB, QuestionDB, TopicDB
        
        topic_stats = {}
        
        attempts = self.db.query(
            QuestionDB.topic_id,
            QuestionDB.id
        ).all()
        
        for topic_id, question_id in attempts:
            if topic_id not in topic_stats:
                topic_stats[topic_id] = 0
            topic_stats[topic_id] += 1
        
        sorted_topics = sorted(topic_stats.items(), key=lambda x: x[1], reverse=True)
        
        trending = []
        for topic_id, count in sorted_topics[:limit]:
            topic = self.db.query(TopicDB).filter(TopicDB.id == topic_id).first()
            if topic:
                trending.append({
                    "topic_id": topic_id,
                    "topic_name": topic.name,
                    "attempt_count": count
                })
        
        return trending
    
    def get_user_learning_path(self, user_id: int) -> dict:
        """Generate a comprehensive learning path for the user."""
        from app import UserProgressDB, SubjectDB
        
        weak_topics = self.identify_weak_topics(user_id, threshold=75.0)
        
        learning_path = {
            "user_id": user_id,
            "weak_topics": [{"topic_id": t[0], "accuracy": t[1]} for t in weak_topics[:10]],
            "next_recommended_questions": self.get_personalized_recommendations(user_id, limit=5),
            "suggested_focus_areas": [t[0] for t in weak_topics[:3]],
            "estimated_hours_needed": len(weak_topics) * 2  # Rough estimate
        }
        
        return learning_path


def update_user_weak_topics(db: Session, user_id: int):
    """Update weak topics for a user based on their recent progress."""
    engine = RecommendationEngine(db)
    weak_topics = engine.identify_weak_topics(user_id, threshold=70.0)
    
    from app import WeakTopicDB
    
    # Clear existing weak topics
    db.query(WeakTopicDB).filter(WeakTopicDB.user_id == user_id).delete()
    
    # Add updated weak topics
    for topic_id, accuracy in weak_topics:
        weak_topic = WeakTopicDB(
            user_id=user_id,
            topic_id=topic_id,
            accuracy_percentage=accuracy
        )
        db.add(weak_topic)
    
    db.commit()

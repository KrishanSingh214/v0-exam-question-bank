import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database import Database

class RecommendationEngine:
    """
    ML-based recommendation engine for suggesting questions based on user performance.
    Uses collaborative filtering and content-based filtering approaches.
    """
    
    def __init__(self):
        self.db = Database()
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000)
        self.question_embeddings = None
        self.user_profiles = {}
    
    def build_user_profile(self, user_id: int):
        """
        Build a user profile based on their performance and preferences.
        Returns a dictionary with user stats and preferences.
        """
        self.db.connect()
        
        # Get user's target exam
        user_query = "SELECT target_exam FROM users WHERE id = %s"
        user = self.db.execute_single(user_query, (user_id,))
        
        if not user:
            self.db.disconnect()
            return None
        
        # Get user's performance stats
        stats_query = """
        SELECT 
            COUNT(*) as total_attempted,
            SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as total_correct,
            AVG(CASE WHEN is_correct THEN 1.0 ELSE 0.0 END) as accuracy_rate
        FROM user_progress WHERE user_id = %s
        """
        stats = self.db.execute_single(stats_query, (user_id,))
        
        # Get topic-wise performance
        topic_stats_query = """
        SELECT 
            t.id,
            t.name,
            COUNT(up.id) as attempted,
            SUM(CASE WHEN up.is_correct THEN 1 ELSE 0 END) as correct,
            ROUND(AVG(CASE WHEN up.is_correct THEN 1.0 ELSE 0.0 END), 2) as accuracy
        FROM topics t
        LEFT JOIN questions q ON t.id = q.topic_id
        LEFT JOIN user_progress up ON q.id = up.question_id AND up.user_id = %s
        WHERE up.id IS NOT NULL
        GROUP BY t.id, t.name
        ORDER BY accuracy ASC
        """
        weak_topics = self.db.execute_query(topic_stats_query, (user_id,))
        
        self.db.disconnect()
        
        profile = {
            "user_id": user_id,
            "target_exam": user['target_exam'],
            "total_attempted": stats['total_attempted'] or 0,
            "total_correct": stats['total_correct'] or 0,
            "overall_accuracy": float(stats['accuracy_rate'] or 0),
            "weak_topics": [dict(t) for t in weak_topics],
            "strong_topics": []
        }
        
        # Identify strong topics (>80% accuracy)
        for topic in weak_topics:
            if topic['accuracy'] >= 0.80:
                profile["strong_topics"].append(dict(topic))
        
        return profile
    
    def calculate_similarity_score(self, question_embeddings, user_question_history):
        """
        Calculate similarity between questions based on content.
        Uses TF-IDF vectorization and cosine similarity.
        """
        if len(user_question_history) == 0:
            return None
        
        # Calculate average embedding of user's attempted questions
        user_vector = np.mean(user_question_history, axis=0)
        
        # Calculate cosine similarity
        similarities = cosine_similarity([user_vector], question_embeddings)[0]
        return similarities
    
    def get_collaborative_recommendations(self, user_id: int, limit: int = 10):
        """
        Get recommendations using collaborative filtering.
        Recommends questions that similar users found helpful.
        """
        self.db.connect()
        
        # Find users with similar target exams and performance levels
        similar_users_query = """
        SELECT u.id
        FROM users u
        WHERE u.target_exam = (SELECT target_exam FROM users WHERE id = %s)
        AND u.id != %s
        AND u.id IN (SELECT DISTINCT user_id FROM user_progress)
        LIMIT 10
        """
        similar_users = self.db.execute_query(similar_users_query, (user_id, user_id))
        
        if not similar_users:
            self.db.disconnect()
            return []
        
        # Get questions answered correctly by similar users but not by this user
        recommendations_query = """
        SELECT q.id, q.topic_id, q.question_text, q.difficulty_level, COUNT(*) as popularity
        FROM questions q
        JOIN user_progress up ON q.id = up.question_id
        WHERE up.user_id IN ({})
        AND up.is_correct = true
        AND q.id NOT IN (SELECT question_id FROM user_progress WHERE user_id = %s)
        GROUP BY q.id, q.topic_id, q.question_text, q.difficulty_level
        ORDER BY popularity DESC, RANDOM()
        LIMIT {}
        """.format(
            ','.join([str(dict(u)['id']) for u in similar_users]),
            limit
        )
        
        recommendations = self.db.execute_query(recommendations_query, (user_id,))
        self.db.disconnect()
        
        return [dict(r) for r in recommendations]
    
    def get_content_based_recommendations(self, user_id: int, limit: int = 10):
        """
        Get recommendations based on content similarity.
        Recommends questions similar to ones the user answered correctly.
        """
        self.db.connect()
        
        # Get questions user answered correctly
        correct_questions_query = """
        SELECT q.question_text
        FROM questions q
        JOIN user_progress up ON q.id = up.question_id
        WHERE up.user_id = %s AND up.is_correct = true
        LIMIT 50
        """
        correct_questions = self.db.execute_query(correct_questions_query, (user_id,))
        
        if not correct_questions:
            self.db.disconnect()
            return []
        
        # Get all unanswered questions
        unanswered_query = """
        SELECT id, question_text, difficulty_level, topic_id
        FROM questions
        WHERE id NOT IN (SELECT question_id FROM user_progress WHERE user_id = %s)
        """
        unanswered = self.db.execute_query(unanswered_query, (user_id,))
        
        self.db.disconnect()
        
        if not unanswered:
            return []
        
        # Calculate TF-IDF similarity
        correct_texts = [q['question_text'] for q in correct_questions]
        unanswered_texts = [q['question_text'] for q in unanswered]
        
        all_texts = correct_texts + unanswered_texts
        
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_texts)
            
            # Calculate average similarity to correct questions
            correct_avg_vector = np.asarray(tfidf_matrix[:len(correct_texts)].mean(axis=0)).ravel()
            unanswered_vectors = tfidf_matrix[len(correct_texts):]
            
            similarities = cosine_similarity([correct_avg_vector], unanswered_vectors)[0]
            
            # Get top similar questions
            top_indices = np.argsort(similarities)[::-1][:limit]
            
            recommendations = [
                {
                    "id": unanswered[idx]['id'],
                    "question_text": unanswered[idx]['question_text'],
                    "difficulty_level": unanswered[idx]['difficulty_level'],
                    "similarity_score": float(similarities[idx])
                }
                for idx in top_indices
            ]
            
            return recommendations
        except:
            return []
    
    def get_hybrid_recommendations(self, user_id: int, limit: int = 10):
        """
        Get recommendations using hybrid approach (collaborative + content-based).
        """
        # Get both types of recommendations
        collaborative = self.get_collaborative_recommendations(user_id, limit // 2)
        content_based = self.get_content_based_recommendations(user_id, limit // 2)
        
        # Combine and deduplicate
        recommendations = {}
        
        for rec in collaborative:
            rec_id = rec['id']
            recommendations[rec_id] = {
                **rec,
                "source": "collaborative",
                "score": len(collaborative) - list(recommendations.keys()).index(rec_id) if rec_id in recommendations else 0
            }
        
        for rec in content_based:
            rec_id = rec['id']
            if rec_id in recommendations:
                recommendations[rec_id]['source'] = 'hybrid'
                recommendations[rec_id]['score'] += rec.get('similarity_score', 0)
            else:
                recommendations[rec_id] = {
                    **rec,
                    "source": "content-based",
                    "score": rec.get('similarity_score', 0)
                }
        
        # Sort by score
        sorted_recs = sorted(recommendations.values(), key=lambda x: x.get('score', 0), reverse=True)
        
        return sorted_recs[:limit]

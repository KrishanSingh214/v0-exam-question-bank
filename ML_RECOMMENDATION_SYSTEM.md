# AI-Powered Recommendation System Explained

## Overview

The Question Bank uses an intelligent recommendation engine that personalizes question suggestions based on each student's performance. Instead of generic "random" questions, it learns from your answers and recommends what you should practice next.

---

## How the Recommendation Algorithm Works

### Step 1: Analyze User Performance

When you answer questions, the system tracks:
- Which topic it belongs to
- Whether you got it right or wrong
- Time spent on the question
- Difficulty level

**Example:**
```
User: John
Questions Attempted: 50

Physics (20 attempts)
├── Mechanics: 18/20 correct = 90% accuracy ✓
├── Optics: 8/12 correct = 67% accuracy ⚠
└── Thermodynamics: 4/8 correct = 50% accuracy ✗

Chemistry (30 attempts)
├── Organic: 25/28 correct = 89% accuracy ✓
├── Inorganic: 3/2 correct = 60% accuracy ⚠
└── Physical: 2/10 correct = 20% accuracy ✗✗
```

### Step 2: Identify Weak Topics

The system calculates accuracy for each topic:
- **Strong** (80%+): You understand this well
- **Moderate** (60-80%): Needs some practice
- **Weak** (<60%): Focus here for improvement

**Algorithm:**
```python
for each topic:
    accuracy = (correct_answers / total_attempts) × 100
    
    if accuracy < 60:
        add to "weak_topics" list
        
sort weak_topics by accuracy (lowest first)
```

### Step 3: Generate Personalized Recommendations

For each weak topic, the system:
1. Finds all unanswered questions from that topic
2. Prioritizes by difficulty (start with easy → progress to hard)
3. Suggests in order of your weakest topics first

**Example Recommendation List:**
```
1. Physical Chemistry - Question 234 (Easy) - Your weakest topic (20%)
2. Physical Chemistry - Question 567 (Medium)
3. Inorganic Chemistry - Question 789 (Easy) - Second weakest (60%)
4. Optics - Question 101 (Medium) - Third weakest (67%)
```

---

## Technical Implementation

### Database Queries for Recommendations

```python
# 1. Get all user attempts
SELECT user_id, question_id, is_correct, topic_id
FROM user_progress
WHERE user_id = 123

# 2. Calculate topic-wise accuracy
SELECT 
    topic_id,
    COUNT(*) as total_attempts,
    SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct_answers,
    (SUM(CASE WHEN is_correct THEN 1 ELSE 0 END)::float / COUNT(*) * 100) as accuracy
FROM user_progress
WHERE user_id = 123
GROUP BY topic_id

# 3. Find weak topics (accuracy < 60%)
SELECT topic_id, accuracy
FROM topic_stats
WHERE accuracy < 60
ORDER BY accuracy ASC

# 4. Get recommended questions
SELECT question_id, difficulty_level, topic_id
FROM questions
WHERE topic_id IN (weak_topic_ids)
AND question_id NOT IN (already_attempted)
ORDER BY difficulty_level ASC
LIMIT 10
```

### How the Backend Implements This

**File:** `backend/routes/recommendations.py`

```python
@router.get("/personalized")
def get_personalized_recommendations(current_user, db):
    # Step 1: Get all user attempts
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()
    
    # Step 2: Calculate topic accuracy
    weak_topics = {}
    for progress in progress_records:
        question = db.query(Question).filter(
            Question.id == progress.question_id
        ).first()
        
        topic_id = question.topic_id
        if topic_id not in weak_topics:
            weak_topics[topic_id] = {"correct": 0, "total": 0}
        
        weak_topics[topic_id]["total"] += 1
        if progress.is_correct:
            weak_topics[topic_id]["correct"] += 1
    
    # Step 3: Identify weak topics (< 60% accuracy)
    low_accuracy_topics = []
    for topic_id, data in weak_topics.items():
        accuracy = (data["correct"] / data["total"] * 100)
        if accuracy < 60:
            low_accuracy_topics.append((topic_id, accuracy))
    
    # Sort by accuracy (weakest first)
    low_accuracy_topics.sort(key=lambda x: x[1])
    
    # Step 4: Get recommended questions
    recommendations = []
    for topic_id, accuracy in low_accuracy_topics[:5]:
        # Get unanswered questions from this topic
        questions = db.query(Question).filter(
            Question.topic_id == topic_id,
            ~Question.id.in_(answered_question_ids)
        ).order_by(Question.difficulty_level).limit(10).all()
        
        recommendations.extend(questions)
    
    return recommendations
```

---

## Recommendation Strategies

### Strategy 1: Weakness-Based (Default)

**Focus:** Your weakest topics first

```
User Accuracy:
- Topic A: 90% → Don't recommend
- Topic B: 70% → Maybe later
- Topic C: 45% → RECOMMEND THIS FIRST!
```

**Why it works:** You learn better by focusing on what you struggle with.

---

### Strategy 2: Difficulty Progression

**Focus:** Easy → Medium → Hard within weak topics

```
Questions from Topic C (45% accuracy):
1. Question 1 (Easy)    ← Start here
2. Question 2 (Easy)
3. Question 3 (Medium)  ← Progress to harder
4. Question 4 (Hard)    ← Challenge yourself
```

**Why it works:** Builds confidence through progressive difficulty.

---

### Strategy 3: Topic Similarity

**Focus:** Topics related to your weak areas

```
If you struggle with Mechanics:
- Also recommend: Circular Motion, Gravity, Energy
- Related to: Kinematics, Forces
```

**Why it works:** Related topics share common concepts.

---

## Real-World Example

### Scenario: JEE Physics Student

**Initial Questions Attempted:**
```
Electronics: 15 correct out of 20 = 75%
Optics: 8 correct out of 20 = 40% ← WEAK
Thermodynamics: 12 correct out of 20 = 60% ← WEAK
Modern Physics: 18 correct out of 20 = 90%
Mechanics: 14 correct out of 20 = 70%
```

**Recommendation Output:**
```json
{
  "personalized_recommendations": [
    {
      "question_id": 534,
      "text": "A light source emits monochromatic light...",
      "topic": "Optics",
      "difficulty": "Easy",
      "reason": "Your weakest topic (40% accuracy)"
    },
    {
      "question_id": 789,
      "text": "An ideal gas undergoes isothermal process...",
      "topic": "Thermodynamics",
      "difficulty": "Easy",
      "reason": "Needs improvement (60% accuracy)"
    },
    // ... more questions ordered by weakness
  ]
}
```

**What Happens Next:**
1. Student solves Optics questions
2. Accuracy improves to 60%
3. System automatically updates recommendations
4. Optics no longer appears at top (you're improving!)
5. Focus shifts to next weak topic

---

## Performance Metrics

### Accuracy Calculation
```
Accuracy = (Correct Answers / Total Attempts) × 100

Example:
Student solved 20 questions
Got 14 correct
Accuracy = (14 / 20) × 100 = 70%
```

### Weak Topic Threshold
```
< 60% = RED (Needs work)
60-75% = YELLOW (Needs practice)
75%+ = GREEN (Good understanding)
```

### Recommendation Refresh
- Recommendations update **immediately** after each answer
- No manual refresh needed
- Real-time learning system

---

## Advanced Features (Coming Soon)

### 1. Time-Based Recommendations
```
If question took too long (>5 minutes):
→ Recommend simpler questions from same topic
→ Break topic into smaller sub-concepts
```

### 2. Peer Comparison
```
"Students with your background usually struggle 
with Optics. Here are the most challenging 
questions on this topic that you should try."
```

### 3. Spaced Repetition
```
Recommend questions you got wrong:
- After 1 day
- After 3 days
- After 1 week
```

### 4. Exam Pattern Recognition
```
"In JEE, Optics questions are 40% calculation, 
60% concept-based. Here are more concept-based 
questions to strengthen that."
```

---

## How to Improve the Recommendations

### As a Student:
1. **Attempt more questions** → More data = better recommendations
2. **Solve questions completely** → Don't skip, commit to an answer
3. **Time yourself** → System learns your speed
4. **Review weak topics** → Actively work on improving

### As an Instructor:
1. **Add quality explanations** → Helps students learn why
2. **Tag questions properly** → Accurate topic/difficulty helps algorithm
3. **Update questions regularly** → Fresh content → Better relevance
4. **Monitor weak topics** → Identify common problem areas

---

## FAQ

**Q: Why am I getting the same questions again?**
A: System recommends from unanswered questions first. If you've answered all easy questions, it moves to medium.

**Q: How do I reset my progress?**
A: Contact admin. They can clear your progress and start fresh.

**Q: Does the system consider how much time I spend?**
A: Yes! Questions you spend too much time on are flagged as "difficult for you" even if correct.

**Q: Can I practice specific topics?**
A: Yes! Use "Browse Questions" to select exact topic you want to practice.

**Q: When will recommendations update?**
A: Immediately after you submit each answer. Next login will show updated list.

---

## Future ML Improvements

1. **Deep Learning**: Use neural networks for pattern recognition
2. **Clustering**: Group similar students and share learning patterns
3. **Prediction**: Predict which questions you'll find difficult
4. **Visualization**: Show learning curves and progress graphs
5. **Adaptive Difficulty**: System adjusts difficulty based on your responses

---

**Summary:** The recommendation system learns from your performance and guides you to practice what you need most. The more you use it, the smarter it becomes! 🎯

# Question Bank - Complete Application Flow

This document shows exactly how the application works, from user action to database update.

---

## 1. User Registration Flow

### User's Perspective
```
User Opens App
    ↓
Clicks "Sign Up"
    ↓
Fills Form:
├── Username
├── Email
├── Password
├── Full Name
└── Target Exam
    ↓
Clicks "Register"
    ↓
Success Message → Redirected to Dashboard
```

### Behind the Scenes
```
Browser (Frontend)
    ↓ POST Request with user data
API Server (Backend)
    ↓ Checks if username already exists
    ├─ YES → Error: "Username taken"
    └─ NO → Continue
    ↓ Hash password with bcrypt
    ↓ INSERT into database
Database (PostgreSQL)
    ↓ Creates user record
    ↓ Returns user ID
    ↓
Backend sends JWT token back
    ↓
Browser stores token
    ↓
User logged in!
```

### Code Example
```python
# Backend receives registration request
@router.post("/register")
def register(user_data):
    # Validate input
    if username_exists(user_data.username):
        raise Error("Username taken")
    
    # Hash password
    hashed_pwd = bcrypt.hash(user_data.password)
    
    # Save to database
    db.user.create(
        username=user_data.username,
        password_hash=hashed_pwd,
        email=user_data.email
    )
    
    # Create token
    token = jwt.create(username)
    
    return {"token": token, "type": "bearer"}

# Frontend stores it
localStorage.setItem("token", response.token)
```

---

## 2. Login Flow

### User's Perspective
```
User Opens App
    ↓
Clicks "Login"
    ↓
Enters Username & Password
    ↓
Clicks "Login"
    ↓
Verification... (2 seconds)
    ↓
Success → Dashboard Opens
```

### Backend Process
```
Frontend → POST /api/auth/login
    ↓
Backend:
1. Query database for username
   ├─ If NOT found → Error "Invalid credentials"
   └─ If found → Continue
   
2. Compare password hashes
   ├─ Matches → Continue
   └─ Doesn't match → Error "Invalid credentials"
   
3. Create new JWT token
   
4. Return token + user info
    ↓
Frontend stores token in localStorage
    ↓
Each future request includes: "Authorization: Bearer <token>"
```

### Security Details
```
Password Flow:
User enters: "MyPassword123"
  ↓
Frontend sends to backend (HTTPS encrypted)
  ↓
Backend NEVER stores plain password
  ↓
Backend hashes it: bcrypt("MyPassword123") = "$2b$12$K1x..."
  ↓
Compares hashes:
  bcrypt.verify("MyPassword123", "$2b$12$K1x...") = true
  ↓
Login successful!

Token Flow:
Token = jwt.encode({
    "username": "john",
    "exp": "2024-12-31",
    "secret_key": "abc123xyz"
})
  ↓
Browser stores: "eyJhbGciOiJIUzI1NiIs..."
  ↓
For each request, includes token
  ↓
Backend verifies signature
  ↓
If tampered, invalid, or expired → Reject
```

---

## 3. Browsing & Viewing Questions

### User's Perspective
```
User on Dashboard
    ↓
Clicks "Browse Questions"
    ↓
Sees filters:
├── Exam: [Select JEE, GATE, CAT]
├── Subject: [Select Physics, Chemistry]
├── Topic: [Select Mechanics, Optics]
├── Difficulty: [Easy / Medium / Hard]
└── Search: [Type keyword]
    ↓
Applies filters
    ↓
Sees list of 20 questions
    ↓
Clicks a question to view details
```

### Backend Process
```
Frontend sends: GET /api/questions?exam=1&subject=2&difficulty=easy

Backend:
1. Build SQL query:
   SELECT * FROM questions
   WHERE exam_id = 1
   AND subject_id = 2
   AND difficulty = 'easy'
   LIMIT 20
   
2. Execute query
3. Return results with options A, B, C, D
4. Also include metadata:
   ├── question_id
   ├── topic_id
   ├── created_date
   └── explanation (optional)

Database Query:
┌─────────────────────────────────┐
│ QUESTIONS Table                 │
├─────────────────────────────────┤
│ id │ text │ exam │ difficulty │
├─────────────────────────────────┤
│ 1  │ Q1   │ GATE │ easy       │ ✓
│ 2  │ Q2   │ JEE  │ easy       │
│ 3  │ Q3   │ GATE │ hard       │
└─────────────────────────────────┘
       ↓
    Return Q1, Q3
```

### Database Query in Detail
```sql
-- What actually runs
SELECT 
    q.id,
    q.question_text,
    q.option_a, q.option_b, q.option_c, q.option_d,
    q.difficulty_level,
    q.subject_id,
    q.topic_id,
    q.exam_id
FROM questions q
WHERE q.exam_id = 1
  AND q.subject_id = 2
  AND q.difficulty_level = 'easy'
ORDER BY q.created_at DESC
LIMIT 20;
```

---

## 4. Solving a Question & Submitting Answer

### User's Perspective
```
Question displayed: "What is velocity?"
Options shown:
A) Rate of change of position ✓ (Correct)
B) Speed in one direction
C) Acceleration over time
D) Distance traveled
    ↓
User reads, thinks...
User clicks: "A"
    ↓
Clicks "Submit Answer"
    ↓
Animation... (1 second)
    ↓
CORRECT! ✓
    ↓
Sees explanation
    ↓
Next button appears
```

### Backend Process
```
Frontend sends:
POST /api/questions/submit-answer
{
    "question_id": 23,
    "answer_given": "A",
    "time_spent_seconds": 45
}

Backend:
1. Get question from database
2. Check: Is answer_given == correct_answer?
   ├─ YES → is_correct = true
   └─ NO → is_correct = false
   
3. Create record in user_progress:
   INSERT INTO user_progress (
       user_id=456,
       question_id=23,
       is_correct=true,
       time_spent_seconds=45,
       attempted_at=NOW()
   )
   
4. Calculate updated accuracy:
   total_attempted = 50
   total_correct = 42
   accuracy = 84%
   
5. Return:
   {
       "is_correct": true,
       "correct_answer": "A",
       "explanation": "Velocity is...",
       "new_accuracy": 84
   }
```

### Database Changes
```
BEFORE submitting:
user_progress table
├── Row 1: Q1, User=456, correct=true
├── Row 2: Q2, User=456, correct=false
└── Row 3: Q3, User=456, correct=true
(Total: 3 records)

USER submits answer to Question 23

AFTER submitting:
user_progress table
├── Row 1: Q1, User=456, correct=true
├── Row 2: Q2, User=456, correct=false
├── Row 3: Q3, User=456, correct=true
└── Row 4: Q23, User=456, correct=true ← NEW
(Total: 4 records)
```

---

## 5. Dashboard & Stats Display

### User's Perspective
```
User clicks "Dashboard"
    ↓
Page loads with:
├── Total Questions Attempted: 50
├── Correct Answers: 42
├── Accuracy: 84%
├── Time Spent: 3 hours 45 minutes
│
├── Weak Topics:
│   ├── Optics (45% accuracy) ← RED
│   ├── Waves (62% accuracy) ← YELLOW
│   └── Mechanics (88% accuracy) ← GREEN
│
├── Recent Activity:
│   ├── Question 5 - Correct ✓ (5 min ago)
│   ├── Question 12 - Incorrect ✗ (10 min ago)
│   └── Question 8 - Correct ✓ (15 min ago)
│
└── "Get Recommendations" button
```

### Backend Calculation Process
```
Frontend: GET /api/users/stats

Backend:
1. Get user's progress records:
   SELECT * FROM user_progress WHERE user_id = 456
   Result: 50 records

2. Count correct answers:
   correct_count = 42

3. Calculate accuracy:
   accuracy = (42 / 50) * 100 = 84%

4. Group by topic:
   Physics:
   ├── Mechanics: 18/20 = 90%
   ├── Optics: 9/20 = 45%
   └── Waves: 15/24 = 62%
   
5. Find weak topics (< 60%):
   weak_topics = [
       {"name": "Optics", "accuracy": 45},
       {"name": "Waves", "accuracy": 62}
   ]

6. Return all stats
```

### Complex Query Example
```sql
-- Calculate accuracy by topic
SELECT 
    t.id,
    t.name,
    COUNT(up.id) as total_questions,
    SUM(CASE WHEN up.is_correct THEN 1 ELSE 0 END) as correct_answers,
    ROUND(
        SUM(CASE WHEN up.is_correct THEN 1 ELSE 0 END)::float / COUNT(up.id) * 100, 
        2
    ) as accuracy_percentage
FROM topics t
LEFT JOIN questions q ON t.id = q.topic_id
LEFT JOIN user_progress up ON q.id = up.question_id
WHERE up.user_id = 456
GROUP BY t.id, t.name
ORDER BY accuracy_percentage ASC;
```

---

## 6. Getting AI Recommendations

### User's Perspective
```
User clicks "Get Recommendations"
    ↓
System analyzes performance...
    ↓
Shows personalized list:
1. "Optics - Question 45" (45% accuracy - START HERE!)
2. "Optics - Question 67" (Your weakest topic)
3. "Waves - Question 89" (62% accuracy - NEXT)
4. "Mechanics - Question 101" (88% accuracy - OPTIONAL)
    ↓
Each has: Difficulty, Topic, Why It's Recommended
```

### Recommendation Algorithm
```
Step 1: Analyze Performance
┌─────────────────────────────────┐
│ User: John                      │
│ Total Attempted: 50             │
│                                 │
│ Physics Topics:                 │
│ ├─ Mechanics: 90%  ✓ Great      │
│ ├─ Optics: 45%     ✗ WEAK       │
│ ├─ Waves: 62%      ⚠ Okay       │
│ └─ Thermodynamics: 88% ✓ Great  │
└─────────────────────────────────┘

Step 2: Identify Weak Topics (< 60%)
Weak_topics = [
    ("Optics", 45%),      ← Lowest
    ("Waves", 62%)
]

Step 3: Sort by Weakness
1st → Optics (45%)
2nd → Waves (62%)

Step 4: Get Unanswered Questions from Weak Topics
For Optics:
  SELECT questions WHERE topic_id=2 AND NOT ANSWERED
  ORDER BY difficulty ASC
  Result: Q45 (Easy), Q67 (Easy), Q89 (Medium)

Step 5: Return Recommendations
Recommendation List:
1. Q45 (Easy, Optics) → "Your weakest topic, start easy"
2. Q67 (Easy, Optics) → "Continue with Optics"
3. Q89 (Medium, Waves) → "Next weak area"
```

### How AI Updates Continuously
```
Timeline:
9:00 AM: Initial stats calculated
         Recommendations: [Q1, Q2, Q3, Q4, Q5]

9:15 AM: User solves Q1 (CORRECT)
         System updates immediately:
         ├─ Q1 no longer recommended
         └─ New Q6 added

9:30 AM: User solves Q2 (INCORRECT)
         System updates:
         ├─ Q2 stays recommended (wrong answer)
         └─ Shows why they got it wrong

9:45 AM: User solves Q3 (CORRECT)
         └─ Q3 replaced with Q7

10:00 AM: Optics accuracy increased to 50%
          ├─ Still weak (< 60%)
          ├─ Shows progress
          └─ Recommendations updated
```

---

## 7. Admin Adding Questions

### Admin's Perspective
```
Admin logs in with special token
    ↓
Goes to Admin Panel
    ↓
Clicks "Add Question"
    ↓
Fills form:
├── Exam: JEE Advanced
├── Subject: Physics
├── Topic: Optics
├── Question Text: "A light ray..."
├── Options: A, B, C, D
├── Correct Answer: C
├── Difficulty: Medium
├── Explanation: "Because..."
    ↓
Clicks "Save"
    ↓
Success! Question now visible to all users
```

### Backend Process
```
Admin sends: POST /api/admin/questions

Backend:
1. Verify admin password
   if password != ADMIN_PASSWORD:
       return Error "Unauthorized"

2. Validate data:
   ├─ Question text not empty? ✓
   ├─ All options provided? ✓
   ├─ Topic exists? ✓
   └─ Correct answer valid? ✓

3. Insert into database:
   INSERT INTO questions (
       exam_id=1,
       subject_id=3,
       topic_id=7,
       question_text='A light ray...',
       option_a='...',
       option_b='...',
       option_c='...',
       option_d='...',
       correct_answer='C',
       difficulty_level='medium',
       explanation='Because...'
   )

4. Return success with question_id=234
```

---

## 8. Complete User Journey Timeline

```
Day 1:
8:00 AM  → Register account
8:05 AM  → Login
8:10 AM  → Browse Physics questions
8:15 AM  → Solve Question 1 (Correct)
8:17 AM  → Solve Question 2 (Correct)
8:20 AM  → Solve Question 3 (Wrong)
         → Accuracy: 67%

Day 2:
9:00 AM  → Login again
9:01 AM  → Check Dashboard
         → Accuracy still 67%
         → Weak topics: Optics, Waves
9:05 AM  → Click "Get Recommendations"
         → System suggests Optics (your weakest)
9:10 AM  → Solve Optics Question 4 (Correct)
         → Accuracy improves
         → System updates recommendations

Day 3:
6:00 PM  → Solve 10 more questions
         → Accuracy: 75%
         → Weak topics: Waves only
         → System recommends Wave questions

Week Later:
         → 200+ questions solved
         → Accuracy: 88%
         → Ready for exam!
```

---

## Data Flow Diagram

```
                    ┌──────────────────┐
                    │   User Computer  │
                    │  (Your Device)   │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Web Browser     │
                    │  (index.html)    │
                    └────────┬─────────┘
                             │ HTTP Requests
                             │
        ┌────────────────────▼────────────────────┐
        │   FastAPI Backend Server                │
        │   (Python on localhost:8000)            │
        │                                          │
        │  ├─ /api/auth       → Auth logic        │
        │  ├─ /api/questions  → Q&A logic         │
        │  ├─ /api/users      → User stats        │
        │  └─ /api/recommendations → AI logic     │
        │                                          │
        └────────────────────┬────────────────────┘
                             │ SQL Queries
                             │
        ┌────────────────────▼────────────────────┐
        │   PostgreSQL Database                   │
        │   (Data Storage)                        │
        │                                          │
        │  ├─ users table                         │
        │  ├─ questions table                     │
        │  ├─ user_progress table                 │
        │  └─ topics/exams tables                 │
        │                                          │
        └─────────────────────────────────────────┘
```

---

## Summary

The Question Bank works in these main cycles:

1. **Registration/Login** → User accounts created and verified
2. **Browse Questions** → Questions fetched from database based on filters
3. **Solve Questions** → Answers submitted and checked against correct answers
4. **Track Progress** → Performance calculated and stored
5. **Get Recommendations** → AI analyzes weak topics and suggests practice
6. **Repeat** → Cycle continues, system learns from more attempts

All communication is **secure** with JWT tokens, and all data is **persistent** in the PostgreSQL database on your computer!


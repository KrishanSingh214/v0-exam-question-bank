# Question Bank - Interactive Demo Guide

## 🎯 Overview

The demo provides a fully functional preview of the Question Bank application. It simulates:
- User authentication (login/registration)
- Question browsing with filtering
- Answer tracking and scoring
- AI-powered recommendations
- Performance analytics with weak topic identification

---

## 🚀 How to Access the Demo

### Option 1: In v0 Preview (Recommended)
1. Open the v0 Preview (right side of the screen)
2. The demo should automatically load at `http://localhost:3000/demo.html`
3. If not, copy the URL from the terminal

### Option 2: On Your Computer
```bash
# Navigate to frontend folder
cd frontend

# Start a simple HTTP server
python3 -m http.server 3000

# Open browser and go to
http://localhost:3000/demo.html
```

---

## 📝 Step-by-Step Demo Walkthrough

### Step 1: Login
When you first open the demo, you'll see the **Login Page**:

```
Login to Question Bank
┌─────────────────────┐
│ Username: demo      │
│ Password: demo123   │
└─────────────────────┘
     [Login Button]
```

**Try these credentials:**
- **Username:** `demo`
- **Password:** `demo123`

Click **Login** to proceed.

---

### Step 2: View Dashboard
After login, you'll see your **Dashboard** with:

#### 📊 Statistics
Shows 3 main metrics:
- **Questions Attempted:** Number of questions you've solved
- **Correct Answers:** How many you got right
- **Accuracy:** Your success percentage

#### 📌 Weak Topics
Displays topics where you scored < 60%:
- **Optics:** 40% accuracy (Weak - needs improvement!)
- **Waves:** 50% accuracy (Below average)

**Progress bar** shows visual representation of your performance in each topic.

#### 🎯 AI Recommendations
Shows personalized question recommendations based on:
- Your weak topics
- Questions you haven't attempted yet
- Increasing difficulty for better learning

---

### Step 3: Browse Questions
Click the **"Browse"** button to see all available questions.

#### Filter Options
You can filter questions by:
- **Subject:** Physics, Chemistry, Mathematics
- **Topic:** Mechanics, Optics, Waves, etc.
- **Difficulty:** Easy, Medium, Hard
- **Keyword Search:** Search question text

#### Question Layout
Each question shows:
```
Question 1 of 9
[Physics] [Mechanics] [Easy]

"A car accelerates from rest at 2 m/s². What is its velocity after 5 seconds?"

○ A) 5 m/s
○ B) 10 m/s      ← Correct answer
○ C) 25 m/s
○ D) 50 m/s
```

---

### Step 4: Answer Questions
1. **Select an option** by clicking on any answer choice
2. **View explanation** - After selection, the correct answer is highlighted in **green** ✓
3. **Read explanation** - Detailed solution appears below the question

#### Answer Feedback System
- **Green (Correct):** Your answer matches the correct answer
- **Red (Incorrect):** You selected the wrong option (if attempted earlier)
- **Blue (Selected):** Current selection (before submission)

---

### Step 5: Track Your Progress
As you answer questions, your dashboard updates automatically:
- **Questions Attempted** increases
- **Correct Answers** increases (if you get it right)
- **Accuracy %** recalculates
- **Weak topics** list updates based on new performance

---

## 💡 How AI Recommendations Work (Demonstrated)

### The Algorithm
```
User solves questions
    ↓
System analyzes accuracy by topic
    ↓
Finds topics with < 60% accuracy
    ↓
Identifies unanswered questions in weak topics
    ↓
Recommends them in order of difficulty (easy first)
    ↓
User practices weak areas
    ↓
Accuracy improves
    ↓
System removes topic from "weak" list
    ↓
Recommends next weak topic
```

### Real Example from Demo
```
Your Topics:
├─ Mechanics: 100% (Strong!) ✓
├─ Optics: 40% (Weak!)        ⚠️ ← Recommended
└─ Waves: 50% (Weak!)         ⚠️ ← Also recommended

System shows:
"Your weak area - 40% accuracy"
Question: "A light ray enters glass..."  ← Recommended to help improve
```

---

## 🔐 Features Demonstrated

### Authentication System
- **Registration:** Create new account with exam interest
- **Login:** Secure login (demo uses simple mock)
- **Session:** Maintains user state across pages
- **Logout:** Clears session and returns to login

### Question Management
- **Filtering:** By subject, topic, difficulty
- **Search:** Full-text search in questions
- **Pagination:** View questions one at a time
- **Categories:** Organized by exam, subject, topic

### Progress Tracking
- **Answer Storage:** Records each answer
- **Accuracy Calculation:** Computes performance percentage
- **Performance History:** Shows which questions you attempted
- **Weak Topic Detection:** Identifies problem areas

### AI Recommendations (Collaborative Filtering)
- **Performance Analysis:** Tracks accuracy by topic
- **Weak Topic Identification:** Topics < 60% accuracy
- **Smart Prioritization:** Recommends weakest topics first
- **Difficulty Progression:** Easy questions before hard ones
- **Dynamic Updates:** Recommendations change as you improve

---

## 📊 Sample Data in Demo

### Available Questions (9 total)

#### Physics - Mechanics (3 questions)
1. **Easy:** Car acceleration (v = u + at)
2. **Easy:** SI units of force
3. **Medium:** Projectile motion at 45°

#### Physics - Optics (3 questions)
4. **Easy:** Speed of light in vacuum
5. **Easy:** Refractive index of water
6. **Medium:** Snell's law calculation

#### Physics - Waves (3 questions)
7. **Easy:** Frequency from wavelength
8. **Easy:** Frequency from period
9. **Medium:** Beat frequency calculation

---

## 🎯 Try These Scenarios

### Scenario 1: Improve Your Weak Topic
1. Go to **Browse**
2. Filter by **Topic: Optics**
3. Answer all 3 Optics questions correctly
4. Return to **Dashboard**
5. Watch your Optics accuracy improve to 100%!

### Scenario 2: Test Search Feature
1. Go to **Browse**
2. In the Search box, type: `light`
3. See only questions containing "light"
4. Try searching: `force`, `wave`, `frequency`

### Scenario 3: Difficulty Progression
1. Go to **Browse**
2. Filter by **Difficulty: Easy**
3. Answer all easy questions
4. Change filter to **Medium**
5. Answer medium questions (harder!)

---

## 🔄 Real Application vs. Demo

| Feature | Demo | Real App |
|---------|------|----------|
| **Questions** | 9 sample | 1000+ from database |
| **Data Storage** | In-memory (JavaScript) | PostgreSQL database |
| **Backend** | Simulated | Python FastAPI |
| **Authentication** | Mock login | Secure JWT tokens |
| **User Data** | Session only | Persistent database |
| **AI Model** | Simple logic | ML-powered recommendations |
| **Multi-user** | One user at a time | Multiple concurrent users |

---

## 🚀 Move from Demo to Real App

Once you understand how the demo works, follow these steps to run the full application:

### 1. Download the Code
```bash
git clone https://github.com/your-repo/question-bank.git
cd question-bank
```

### 2. Install Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Seed Database with Demo Data
```bash
python scripts/seed_demo_data.py
```

### 4. Start Backend
```bash
python main.py
# Runs on http://localhost:8000
```

### 5. Start Frontend
```bash
cd ../frontend
python -m http.server 3000
# Open http://localhost:3000/index.html
```

### 6. Login with Demo Credentials
- **Username:** `demo`
- **Password:** `demo123`

---

## 📚 What You'll See

### Login Page
- Clean, modern interface
- Fields for username and password
- Quick registration option

### Dashboard Page
- Your performance statistics
- List of weak topics with accuracy
- AI-powered recommendations
- Quick access to practice

### Browse Page
- Advanced filtering system
- Full-text search
- 1000+ real exam questions
- Detailed explanations

### Admin Page (Backend Only)
- Add/edit/delete questions
- Manage exams and subjects
- View platform statistics

---

## ❓ Common Questions About Demo

**Q: Will my progress be saved?**
A: Only during your session. Refresh the page and it resets. The real app saves to database.

**Q: Why only 9 questions?**
A: This is a demo. The real app has 1000+ questions from actual exams.

**Q: How do recommendations work?**
A: Accuracy < 60% = weak. System recommends unanswered questions from weak topics.

**Q: Can I add questions?**
A: In the real app, yes via admin panel. Demo doesn't have this feature.

**Q: Is my data private?**
A: Demo = browser only. Real app = your PostgreSQL database on your computer.

---

## 🎓 Learning Path

1. **Explore Demo** (5 min) - Get familiar with UI
2. **Answer Some Questions** (10 min) - See how filtering works
3. **Check Dashboard** (5 min) - Understand metrics
4. **Read Documentation** (10 min) - Learn architecture
5. **Download & Setup** (30 min) - Install real app locally
6. **Add Your Questions** (30 min) - Load exam questions
7. **Start Studying** (∞) - Use for exam prep!

---

## 📞 Support

If you have questions:
1. Read **QUICK_START_GUIDE.md** - Setup help
2. Check **APPLICATION_FLOW.md** - How features work
3. See **ML_RECOMMENDATION_SYSTEM.md** - AI explanation
4. Review **PROJECT_SUMMARY.md** - Technical details

---

## ✅ Demo Checklist

- [ ] Opened demo in browser
- [ ] Logged in with demo credentials
- [ ] Viewed dashboard and statistics
- [ ] Browsed questions
- [ ] Filtered by different criteria
- [ ] Answered at least 3 questions
- [ ] Saw explanation for answers
- [ ] Checked recommendations
- [ ] Registered a new account
- [ ] Understood how recommendations work

**All done?** You're ready to download and run the full application! 🚀

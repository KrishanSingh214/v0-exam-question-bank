# Question Bank - Quick Start Guide

## Overview
The Question Bank is a full-stack web application designed to help students prepare for exams. It has:
- **Frontend**: HTML/CSS/JavaScript running in your browser
- **Backend**: Python FastAPI server handling all logic
- **Database**: PostgreSQL storing all questions and user data

## System Requirements
- **Python 3.8+** (for backend)
- **PostgreSQL 12+** (for database)
- **Node.js/npm** (optional, for development tools)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Git** (to clone the repository)

---

## Installation Steps

### Step 1: Install Prerequisites

#### On Windows:
1. **Python**: Download from https://www.python.org/downloads/
   - ✓ Check "Add Python to PATH"
   - Run installer
   
2. **PostgreSQL**: Download from https://www.postgresql.org/download/windows/
   - Install with default settings
   - Remember the password for 'postgres' user
   
3. **Git**: Download from https://git-scm.com/download/win

#### On macOS:
```bash
# Using Homebrew (install from https://brew.sh if you don't have it)
brew install python@3.11
brew install postgresql
brew install git
```

#### On Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install postgresql postgresql-contrib
sudo apt install git
```

---

### Step 2: Download the Application

```bash
# Clone the repository
git clone <your-repo-url> question-bank
cd question-bank
```

Or if you have a ZIP file:
1. Extract the ZIP file to your desired location
2. Open terminal/command prompt in that folder

---

### Step 3: Setup PostgreSQL Database

#### On Windows (using pgAdmin - GUI):
1. Open pgAdmin (comes with PostgreSQL)
2. Right-click "Databases" → Create → Database
3. Enter name: `question_bank`
4. Click Save

#### On macOS/Linux (using terminal):
```bash
# Connect to PostgreSQL
psql -U postgres

# In the psql prompt:
CREATE DATABASE question_bank;
\q
```

---

### Step 4: Setup Backend (Python)

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 5: Configure Environment Variables

Create a `.env` file in the `backend` folder with the following content:

```ini
# Database Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/question_bank
DB_HOST=localhost
DB_PORT=5432
DB_NAME=question_bank
DB_USER=postgres
DB_PASSWORD=your_password

# Security (change these in production!)
SECRET_KEY=your-secret-key-change-this-in-production-12345
ADMIN_PASSWORD=admin123

# Server Configuration
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Token Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Replace `your_password` with the PostgreSQL password you created during installation.**

---

### Step 6: Initialize Database Schema

```bash
# Still in backend folder with virtual environment activated
python -c "from main import app; from database import init_db; init_db()"
```

Or run the SQL script directly:
```bash
psql -U postgres -d question_bank -f database/schema.sql
```

---

### Step 7: Load Sample Questions

```bash
# In backend folder
python scripts/import_questions.py
```

This will load sample exam questions into the database.

---

### Step 8: Start the Backend Server

```bash
# In backend folder with virtual environment activated
python -m uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

### Step 9: Open the Frontend

1. Navigate to the `frontend` folder
2. Open `index.html` in your web browser

**Or** use a simple Python server to serve it properly:
```bash
# In frontend folder (open new terminal)
cd ../frontend
python -m http.server 3000
```

Then visit: `http://localhost:3000`

---

## How to Use the Application

### 1. **Register as a New User**
- Click "Sign Up" on the home page
- Enter your details:
  - Username
  - Email
  - Password
  - Full Name
  - Target Exam (e.g., "GATE", "JEE", "CAT")
  - Subject of Interest (optional)

### 2. **Browse Questions**
- Go to "Browse Questions" section
- Filter by:
  - Exam type
  - Subject
  - Topic
  - Difficulty level (Easy, Medium, Hard)
  - Keyword search

### 3. **Solve Questions**
- Click on any question to see details
- View the 4 options (A, B, C, D)
- Submit your answer
- Get instant feedback on correctness
- View explanation

### 4. **Track Progress**
- Dashboard shows:
  - Total questions attempted
  - Accuracy percentage
  - Questions correct vs incorrect
  - Weak topics (< 60% accuracy)

### 5. **Get Personalized Recommendations**
- System analyzes your performance
- Recommends questions from weak topics first
- Helps you focus on problem areas

### 6. **Bookmark Questions**
- Click bookmark icon to save important questions
- Review saved questions anytime

### 7. **Admin Panel** (for instructors/admins)
- Add new exams, subjects, topics
- Upload new questions
- Manage existing questions
- View platform statistics

**Admin Password**: `admin123` (change in production!)

---

## How the System Works

### Architecture Overview

```
┌─────────────────────┐
│   Web Browser       │
│  (Frontend HTML/    │
│   CSS/JavaScript)   │
└──────────┬──────────┘
           │ HTTP Requests/Responses
           ▼
┌─────────────────────┐
│  FastAPI Backend    │
│  (Python Server)    │
│  - Authentication   │
│  - Question Logic   │
│  - Recommendations  │
└──────────┬──────────┘
           │ SQL Queries
           ▼
┌─────────────────────┐
│  PostgreSQL DB      │
│  - Users            │
│  - Questions        │
│  - Progress         │
│  - Bookmarks        │
└─────────────────────┘
```

### Step-by-Step Flow

#### **User Registration & Login**
1. User enters credentials in frontend
2. Frontend sends to backend: `POST /api/auth/register`
3. Backend:
   - Validates input
   - Hashes password using bcrypt
   - Stores in database
   - Returns JWT token
4. Frontend stores token in browser
5. Token used for all future authenticated requests

#### **Viewing Questions**
1. User filters questions (by exam, subject, difficulty)
2. Frontend sends: `GET /api/questions?exam_id=1&difficulty=easy`
3. Backend queries database
4. Returns questions with 4 options
5. Frontend displays in browser

#### **Submitting Answers**
1. User selects an option and clicks "Submit"
2. Frontend sends: `POST /api/questions/submit-answer?question_id=1&answer_given=A`
3. Backend:
   - Compares answer with correct answer
   - Records in `user_progress` table
   - Calculates accuracy
   - Returns result: `{"is_correct": true, "correct_answer": "A"}`
4. Frontend shows feedback

#### **Recommendations**
1. User goes to "Recommended Questions"
2. Frontend sends: `GET /api/recommendations/personalized`
3. Backend:
   - Analyzes all user attempts
   - Calculates accuracy per topic
   - Finds topics with < 60% accuracy
   - Suggests unanswered questions from weak topics
   - Returns personalized list
4. Frontend displays recommendations

### Database Structure

```
USERS Table
├── id, username, email
├── password_hash
├── full_name
├── exam_interest
└── created_at

EXAMS Table
├── id, name (GATE, JEE, CAT, etc.)
└── description

SUBJECTS Table
├── id, name
├── exam_id (which exam)
└── description

TOPICS Table
├── id, name
├── subject_id (which subject)
└── description

QUESTIONS Table
├── id, question_text
├── option_a, option_b, option_c, option_d
├── correct_answer (A/B/C/D)
├── difficulty_level (easy/medium/hard)
├── exam_id, subject_id, topic_id
└── explanation

USER_PROGRESS Table
├── id, user_id, question_id
├── is_correct (true/false)
├── time_spent_seconds
└── attempted_at

BOOKMARKS Table
├── id, user_id, question_id
└── created_at
```

### Key Features Explained

#### **1. Search & Filter**
- Uses SQL `ILIKE` for text search
- Filters with `WHERE` clauses
- Fast due to database indexes

#### **2. Progress Tracking**
- Each answer stored with timestamp
- Calculates accuracy: `correct_answers / total_attempts * 100`
- Groups by topic to find weak areas

#### **3. AI Recommendations**
- Collaborative filtering approach:
  - Identifies topics with < 60% accuracy
  - Prioritizes unanswered questions
  - Orders by difficulty (easy → hard)
- Content-based filtering:
  - Suggests similar topics based on performance

#### **4. Authentication**
- JWT tokens expire in 30 minutes
- Password hashed with bcrypt (not stored in plain text)
- Token required for all protected endpoints

#### **5. Admin Features**
- Restricted with admin password
- Can add/edit/delete questions
- Can manage exams, subjects, topics
- View platform statistics

---

## Common Issues & Solutions

### Issue: "Cannot connect to database"
**Solution:**
1. Make sure PostgreSQL is running
2. Check username/password in .env file
3. Verify database name exists

### Issue: "ModuleNotFoundError" for libraries
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Frontend can't connect to backend
**Solution:**
1. Make sure backend is running (check `http://localhost:8000/health`)
2. Check CORS settings in backend .env
3. Check frontend API_URL in `js/config.js`

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Use different port
python -m uvicorn main:app --reload --port 9000
```

---

## Next Steps

1. **Load More Questions**: Use the import script to add real exam questions
2. **Customize**: Modify colors/styling in `frontend/css/styles.css`
3. **Deploy**: Deploy to Heroku, AWS, or DigitalOcean
4. **Scale**: Add more features like forums, live quizzes, etc.

---

## Support

For issues:
1. Check terminal/console for error messages
2. Verify all prerequisites are installed
3. Ensure database is running
4. Check network requests in browser DevTools

Happy studying! 📚

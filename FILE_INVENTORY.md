# Question Bank - Complete File Inventory

This document provides a complete listing of all files in the project with descriptions.

---

## 📋 Overview

**Total Files**: 20+
**Total Lines of Code**: 4,000+
**Documentation**: 1,700+ lines
**Languages**: Python, JavaScript, SQL, HTML, CSS

---

## 📁 Directory Structure

```
question-bank/
├── frontend/                 # Frontend application
├── backend/                  # Backend API server
├── database/                 # Database schema
├── docker-compose.yml        # Docker orchestration
├── nginx.conf               # Web server configuration
├── README.md                # Full documentation
├── SETUP_GUIDE.md          # Detailed setup instructions
├── QUICKSTART.md           # Quick start guide
├── IMPLEMENTATION_SUMMARY.md # Architecture overview
└── FILE_INVENTORY.md       # This file
```

---

## 📂 Frontend Files

### frontend/index.html (246 lines)
**Purpose**: Main HTML structure and UI layout

**Contains**:
- Navigation bar with authentication menu
- Home page with hero section and features
- Dashboard page with user statistics
- Browse questions page with filters
- Question detail page with answer form
- Bookmarks page
- Modal forms for login/register
- Toast notification element

**Features**:
- Semantic HTML5
- Accessibility features (ARIA labels)
- Modal structure for overlays
- Form inputs with proper labels
- Dynamic element IDs for JavaScript binding

**Key Sections**:
- `<nav class="navbar">` - Navigation
- `<section id="home">` - Home page
- `<section id="dashboard">` - User dashboard
- `<section id="browse">` - Question browser
- `<section id="questionDetail">` - Question details
- `<div id="loginModal">` - Auth modal
- `<div id="toast">` - Notifications

---

### frontend/styles.css (674 lines)
**Purpose**: Complete responsive styling

**Includes**:
- CSS variables for color system
- Responsive grid and flexbox layouts
- Mobile-first media queries
- Component styles (cards, buttons, forms)
- Animation and transition effects
- Accessibility features (focus states)

**Color Scheme**:
- Primary: #2563eb (Blue)
- Secondary: #64748b (Gray)
- Success: #10b981 (Green)
- Error: #ef4444 (Red)
- Warning: #f59e0b (Amber)

**Features**:
- CSS variables for theming
- Responsive breakpoints (480px, 768px)
- Flexbox layouts
- Grid for multi-column sections
- Smooth transitions and animations
- Accessible color contrast
- Print-friendly styles

**Component Styles**:
- `.navbar` - Navigation bar
- `.btn`, `.btn-primary`, `.btn-secondary` - Buttons
- `.card` - Card components
- `.modal` - Modal dialogs
- `.form-group` - Form fields
- `.feature-card` - Feature cards
- `.stat-card` - Statistics display
- `.question-card` - Question preview
- `.option` - Multiple choice option
- `.toast` - Notification

---

### frontend/app.js (543 lines)
**Purpose**: Client-side application logic

**Core Functionality**:
- Authentication (login, register, logout)
- Page navigation
- API communication via Fetch
- State management
- Form handling
- Data display

**Constants**:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
const STORAGE_KEY = 'qb_user';
const TOKEN_KEY = 'qb_token';
```

**Main Functions**:

**Auth Functions**:
- `handleLogin()` - Process login form
- `handleRegister()` - Process registration
- `logout()` - User logout
- `updateAuthUI()` - Update nav based on auth state

**Page Functions**:
- `navigateTo(pageId)` - Navigate between pages
- `displayQuestions()` - Show question list
- `viewQuestion()` - Show question detail
- `displayQuestionDetail()` - Render full question
- `submitAnswer()` - Submit answer and check

**Data Loading**:
- `loadExams()` - Fetch available exams
- `loadSubjects()` - Fetch subjects for exam
- `loadTopics()` - Fetch topics for subject
- `loadQuestions()` - Fetch questions with filters
- `loadUserProgress()` - Fetch user statistics
- `loadRecommendations()` - Get AI recommendations
- `loadBookmarks()` - Fetch user bookmarks

**Bookmark Functions**:
- `toggleBookmark()` - Add/remove bookmark
- `loadBookmarks()` - Show bookmarked questions

**Utility Functions**:
- `showToast()` - Display notification

**Event Handlers**:
- Modal open/close handlers
- Form submission handlers
- Filter change handlers
- Question click handlers

---

## 🔧 Backend Files

### backend/app.py (509 lines)
**Purpose**: FastAPI server with all endpoints

**Imports**:
```python
from fastapi import FastAPI
from sqlalchemy import create_engine
from pydantic import BaseModel
import jwt, bcrypt
```

**Database Models** (SQLAlchemy):
- `UserDB` - User accounts
- `ExamDB` - Exams
- `SubjectDB` - Subjects
- `TopicDB` - Topics
- `QuestionDB` - Questions
- `OptionDB` - Multiple choice options
- `UserProgressDB` - Answer history
- `BookmarkDB` - Saved questions
- `WeakTopicDB` - Weak areas
- `QuizSessionDB` - Quiz attempts

**Pydantic Models** (Request/Response):
- `UserRegister` - Registration request
- `UserLogin` - Login request
- `UserResponse` - User response
- `TokenResponse` - Auth response
- `QuestionResponse` - Question list item
- `OptionResponse` - Question option
- `QuestionDetailResponse` - Full question

**API Routes**:

**Authentication (2)**:
- POST `/api/auth/register` - User registration
- POST `/api/auth/login` - User login

**Questions (2)**:
- GET `/api/questions` - List with filters
- GET `/api/questions/{id}` - Detail view

**Exams & Organization (3)**:
- GET `/api/exams` - List exams
- GET `/api/exams/{id}/subjects` - Exam subjects
- GET `/api/subjects/{id}/topics` - Subject topics

**User Progress (2)**:
- POST `/api/progress/submit` - Submit answer
- GET `/api/progress/user` - User statistics

**Recommendations (1)**:
- GET `/api/recommendations` - Get recommendations

**Bookmarks (3)**:
- POST `/api/bookmarks/{id}` - Add bookmark
- DELETE `/api/bookmarks/{id}` - Remove bookmark
- GET `/api/bookmarks` - List bookmarks

**Health Check (1)**:
- GET `/health` - API status

**Security Features**:
- JWT token generation and verification
- Bcrypt password hashing
- CORS middleware
- Input validation with Pydantic
- SQLAlchemy ORM protection

**Key Functions**:
- `hash_password()` - Hash passwords
- `verify_password()` - Check passwords
- `create_access_token()` - Generate JWT
- `verify_token()` - Validate JWT
- `get_db()` - Database session dependency

---

### backend/ml_recommender.py (224 lines)
**Purpose**: Machine learning recommendation engine

**Main Class**: `RecommendationEngine`

**Methods**:

1. **calculate_topic_accuracy(user_id, topic_id)**
   - Calculates accuracy percentage for a topic
   - Returns float (0-100)
   - Default 50% for untested topics

2. **identify_weak_topics(user_id, threshold=70)**
   - Finds topics below accuracy threshold
   - Returns list of (topic_id, accuracy) tuples
   - Sorted by lowest accuracy first

3. **get_personalized_recommendations(user_id, limit=10)**
   - Main recommendation function
   - Gets weak topics
   - Selects unanswered questions from weak areas
   - Returns list of question IDs

4. **_get_difficulty_based_recommendations(user_id, limit=10)**
   - Fallback for users with no weak topics
   - Adjusts difficulty based on overall accuracy
   - Easy (< 50%), Medium (< 75%), Hard (>= 75%)

5. **content_similarity_recommendations(question_id, limit=5)**
   - Finds similar questions
   - Matches topic and difficulty
   - Returns related questions

6. **get_trending_topics(limit=5)**
   - Gets most popular topics
   - Based on attempt counts
   - Returns topic stats

7. **get_user_learning_path(user_id)**
   - Generates comprehensive learning roadmap
   - Identifies weak areas
   - Estimates study hours
   - Suggests focus areas

**Algorithm Details**:

**Weak Topic Detection**:
```python
for topic in all_topics:
    accuracy = correct_answers / total_attempts
    if accuracy < 70%:
        weak_topics.append(topic)
```

**Recommendation Logic**:
```python
1. Get all weak topics
2. Update database with accuracy percentages
3. Query unanswered questions from weak topics
4. Sort by difficulty (highest first)
5. Return top N questions
```

**Difficulty Progression**:
```
Accuracy < 50% → Recommend Easy questions
50% ≤ Accuracy < 75% → Recommend Medium questions
Accuracy ≥ 75% → Recommend Hard questions
```

**Utility Function**:
- `update_user_weak_topics(db, user_id)` - Updates weak topics in DB

---

### backend/import_sample_data.py (367 lines)
**Purpose**: Populate database with sample data

**Main Function**: `main()`

**Import Functions**:

1. **import_exams()** (4 exams)
   - SAT, GRE, TOEFL, IELTS
   - Returns exam objects

2. **import_subjects()** (10 subjects)
   - English, Math, Reading, Listening, etc.
   - Linked to exams

3. **import_topics()** (25+ topics)
   - Grammar, Algebra, Geometry, etc.
   - Linked to subjects

4. **import_sample_questions()** (8 questions)
   - Grammar, Vocabulary, Math
   - Complete with options
   - Marked with correct answer

5. **generate_more_questions()** (Additional questions)
   - Fills database with variety
   - Multiple options per topic

**Output**:
```
✓ Imported 4 exams
✓ Imported 10 subjects
✓ Imported 25+ topics
✓ Imported 50+ sample questions
✓ Generated additional sample questions
```

---

### backend/pdf_parser.py (336 lines)
**Purpose**: Parse PDF question files and export to CSV

**Main Class**: `QuestionParser`

**Methods**:

1. **parse_english_format(text)**
   - Extracts English questions from text
   - Format: "1. Question? (a) Option A (b) Option B..."
   - Returns list of question dicts

2. **parse_math_format(text)**
   - Extracts Math questions
   - Determines difficulty from keywords
   - Returns question dicts

3. **extract_from_text_file(filepath)**
   - Reads text file
   - Routes to appropriate parser
   - Returns questions

4. **to_csv(output_path, questions)**
   - Exports to CSV format
   - Creates columns for all fields
   - Returns True on success

**Helper Class**: `PDFToCSVConverter`

**Methods**:
- `convert_english_pdfs()` - Convert English questions
- `convert_math_pdfs()` - Convert Math questions

**CSV Output Format**:
```
question_number, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, subject, topic, type
```

**Usage**:
```bash
python pdf_parser.py input.txt output.csv
```

---

### backend/requirements.txt (17 lines)
**Purpose**: Python dependencies

**Packages**:
- fastapi==0.104.1 - Web framework
- uvicorn==0.24.0 - ASGI server
- psycopg2-binary==2.9.9 - PostgreSQL driver
- python-dotenv==1.0.0 - Environment variables
- pydantic==2.5.0 - Data validation
- python-jose==3.3.0 - JWT library
- passlib==1.7.4 - Password utilities
- bcrypt==4.1.1 - Password hashing
- sqlalchemy==2.0.23 - ORM
- alembic==1.12.1 - Database migrations
- pyjwt==2.8.1 - JWT tokens
- numpy==1.26.2 - Numerical computing
- scikit-learn==1.3.2 - ML algorithms
- pandas==2.1.3 - Data analysis

**Installation**:
```bash
pip install -r requirements.txt
```

---

### backend/.env.example (11 lines)
**Purpose**: Environment configuration template

**Variables**:
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=0.0.0.0
PORT=8000
DEBUG=False
CORS_ORIGINS=*
```

**Usage**:
```bash
cp .env.example .env
# Edit .env with your values
```

---

### backend/Dockerfile (25 lines)
**Purpose**: Container image definition

**Components**:
- Python 3.11 slim base image
- System dependencies installation
- Python dependencies installation
- Application code copying
- Port exposure (8000)
- Startup command

---

## 📚 Database Files

### database/schema.sql (133 lines)
**Purpose**: PostgreSQL database schema

**Tables** (10):

1. **users**
   - Columns: id, username, email, password_hash, full_name, target_exam, created_at, updated_at
   - Indexes: email, username
   - Primary key: id

2. **exams**
   - Columns: id, name, description, category, created_at
   - Index: name
   - Unique: name

3. **subjects**
   - Columns: id, exam_id, name, description
   - Foreign key: exam_id → exams
   - Index: exam_id, name

4. **topics**
   - Columns: id, subject_id, name, description
   - Foreign key: subject_id → subjects
   - Index: subject_id, name

5. **questions**
   - Columns: id, topic_id, question_text, question_type, difficulty_level, explanation, created_at
   - Foreign key: topic_id → topics
   - Index: topic_id

6. **options**
   - Columns: id, question_id, option_text, option_label, is_correct
   - Foreign key: question_id → questions
   - Index: question_id

7. **user_progress**
   - Columns: id, user_id, question_id, exam_id, answer_selected, is_correct, attempts, last_attempted, time_spent_seconds
   - Foreign keys: user_id, question_id, exam_id
   - Unique: (user_id, question_id)
   - Indexes: user_id, question_id

8. **bookmarks**
   - Columns: id, user_id, question_id, created_at
   - Foreign keys: user_id, question_id
   - Unique: (user_id, question_id)
   - Index: user_id

9. **weak_topics**
   - Columns: id, user_id, topic_id, accuracy_percentage, last_updated
   - Foreign keys: user_id, topic_id
   - Unique: (user_id, topic_id)
   - Index: user_id

10. **quiz_sessions**
    - Columns: id, user_id, exam_id, topic_id, total_questions, correct_answers, score, duration_seconds, started_at, completed_at
    - Foreign keys: user_id, exam_id, topic_id
    - Index: user_id

**Features**:
- Proper foreign key relationships
- Cascading deletes where appropriate
- Strategic indexing for performance
- Unique constraints to prevent duplicates
- Timestamps for tracking

---

## 🐳 Docker & Deployment Files

### docker-compose.yml (67 lines)
**Purpose**: Multi-container orchestration

**Services**:
1. **postgres** - PostgreSQL database
   - Image: postgres:15-alpine
   - Port: 5432
   - Volume: postgres_data
   - Healthcheck included

2. **backend** - FastAPI server
   - Build from ./backend/Dockerfile
   - Port: 8000
   - Depends on: postgres
   - Auto-reload enabled

3. **frontend** - Nginx web server
   - Image: nginx:alpine
   - Port: 3000
   - Volume: ./frontend
   - Reverse proxy configured

**Network**: qb_network (bridge)

**Volumes**: postgres_data

---

### nginx.conf (50 lines)
**Purpose**: Web server and reverse proxy configuration

**Features**:
- Static file serving for frontend
- API request proxying to backend
- GZIP compression
- WebSocket support
- Cache headers for static files
- Client body size limit

---

## 📖 Documentation Files

### README.md (407 lines)
**Sections**:
- Feature overview
- Tech stack details
- Installation instructions
- Database schema explanation
- API endpoints documentation
- Usage guide
- ML algorithms explanation
- Configuration reference
- Deployment instructions
- Troubleshooting guide
- Contributing guidelines

### SETUP_GUIDE.md (484 lines)
**Sections**:
- Docker quick start
- Manual setup (6 steps)
- Database configuration
- Backend setup
- Frontend setup
- Testing instructions
- Configuration reference
- Troubleshooting guide
- Production deployment
- Development tips
- Quick reference commands

### QUICKSTART.md (276 lines)
**Sections**:
- Ultra quick start (Docker)
- Manual setup steps
- First steps tutorial
- API testing examples
- Troubleshooting tips
- Documentation links
- Next steps suggestions

### IMPLEMENTATION_SUMMARY.md (556 lines)
**Sections**:
- Project overview
- Complete component breakdown
- Technology stack
- Key features checklist
- Project structure
- Getting started options
- API documentation
- Sample data included
- ML algorithm explanation
- Performance optimization
- Security features
- Testing checklist
- Deployment readiness
- File summary table
- Support resources

### FILE_INVENTORY.md (This file)
**Purpose**: Complete documentation of all files

---

## 📊 Statistics

### Code Distribution
- **Frontend**: 1,463 lines (HTML, CSS, JS)
- **Backend**: 2,032 lines (Python)
- **Database**: 133 lines (SQL)
- **Documentation**: 1,700+ lines (Markdown)
- **Configuration**: 150 lines (YAML, Config)

### File Count
- **Python Files**: 4 (app.py, ml_recommender.py, pdf_parser.py, import_sample_data.py)
- **JavaScript Files**: 1 (app.js)
- **HTML Files**: 1 (index.html)
- **CSS Files**: 1 (styles.css)
- **SQL Files**: 1 (schema.sql)
- **YAML/Config Files**: 3 (docker-compose.yml, nginx.conf, .env.example)
- **Documentation**: 5 (README, SETUP_GUIDE, QUICKSTART, IMPLEMENTATION_SUMMARY, FILE_INVENTORY)

### API Endpoints
- Total: 15+
- Auth: 2
- Questions: 2
- Organization: 3
- Progress: 2
- Recommendations: 1
- Bookmarks: 3
- Health: 1

### Database Tables
- Total: 10
- Relationships: Fully normalized
- Indexes: 12 strategic indexes
- Constraints: Unique, Foreign Key, NOT NULL

---

## 🎯 Usage Summary

| Task | Files Involved |
|------|----------------|
| Run Application | docker-compose.yml, Dockerfile |
| Develop Frontend | frontend/* |
| Develop Backend | backend/app.py, ml_recommender.py |
| Add Data | backend/import_sample_data.py, pdf_parser.py |
| Configure | backend/.env.example, nginx.conf |
| Deploy | docker-compose.yml, README.md, SETUP_GUIDE.md |
| Understand Architecture | IMPLEMENTATION_SUMMARY.md |
| Quick Start | QUICKSTART.md |
| Setup Details | SETUP_GUIDE.md |
| API Reference | README.md, backend/app.py |

---

## ✅ File Checklist

- ✅ Frontend: HTML, CSS, JavaScript
- ✅ Backend: FastAPI server, ML engine, data import
- ✅ Database: Schema with 10 tables
- ✅ Deployment: Docker, nginx configuration
- ✅ Configuration: Environment template
- ✅ Documentation: 5 detailed guides
- ✅ Dependencies: Python requirements listed
- ✅ Sample Data: Pre-populated database script

---

**All files are in place and ready for deployment!**

See QUICKSTART.md to get started in 2 minutes.

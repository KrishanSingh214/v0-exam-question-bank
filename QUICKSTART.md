# Question Bank - Quick Start Guide

Get the application running in **5 minutes** with Docker or **15 minutes** manually.

---

## ⚡ Ultra Quick Start (Docker) - 2 Minutes

**Requirements**: Docker and Docker Compose installed

```bash
# 1. Navigate to project directory
cd question-bank

# 2. Start everything
docker-compose up

# 3. Open browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs

# 4. Create account and start learning!
```

**Done!** Your full-stack application is running.

To stop: Press `Ctrl+C`

---

## 🔧 Manual Setup - 15 Minutes

### Step 1: Database (3 minutes)

```bash
# Create database
psql -U postgres -c "CREATE DATABASE question_bank;"

# Load schema
psql -U postgres -d question_bank -f database/schema.sql

# Verify
psql -U postgres -d question_bank -c "\dt"
# Should show: users, questions, exams, subjects, topics, options, etc.
```

### Step 2: Backend (5 minutes)

```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup config
cp .env.example .env
# Edit .env and update DATABASE_URL

# Import sample data
python import_sample_data.py

# Start server
python app.py
# Should show: "Uvicorn running on http://0.0.0.0:8000"
```

### Step 3: Frontend (2 minutes)

```bash
cd frontend

# Serve with Python
python -m http.server 3000

# Or with Node.js http-server
npm install -g http-server
http-server -p 3000
```

### Step 4: Visit Application

Open browser: **http://localhost:3000**

---

## 🎯 First Steps

1. **Register Account**
   - Click "Get Started"
   - Enter details
   - Select target exam (SAT, GRE, TOEFL)
   - Click "Register"

2. **Browse Questions**
   - Go to "Browse" tab
   - Select Exam → Subject → Topic
   - Choose difficulty level
   - Click a question

3. **Answer Questions**
   - Read question
   - Select answer option
   - Click "Submit Answer"
   - See if correct immediately

4. **View Progress**
   - Go to "Dashboard"
   - See your accuracy, attempts, weak topics
   - Get AI recommendations

5. **Bookmark Questions**
   - Click 📌 button on any question
   - Go to "Bookmarks" tab to review later

---

## 🔌 API Testing

### Swagger UI (Auto-Generated)
Visit: http://localhost:8000/docs

Try any endpoint from the browser!

### Example Requests

**Create Account**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "target_exam": "SAT"
  }'
```

**Get Questions**:
```bash
curl http://localhost:8000/api/questions?difficulty=Easy&limit=5
```

---

## 📊 Database Sample Data

Pre-loaded with:
- 4 Exams (SAT, GRE, TOEFL, IELTS)
- 10 Subjects
- 25+ Topics
- 50+ Sample Questions

All ready to use!

---

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Change port
python -m http.server 3001  # Frontend on 3001
uvicorn app:app --port 8001  # Backend on 8001

# Update API_BASE_URL in frontend/app.js
const API_BASE_URL = 'http://localhost:8001/api';
```

### Database Connection Error
```bash
# Check PostgreSQL
psql -U postgres

# Check DATABASE_URL in backend/.env
# Format: postgresql://user:password@localhost:5432/question_bank

# Test connection
psql "postgresql://postgres:password@localhost:5432/question_bank"
```

### Frontend Not Loading Questions
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab → API calls
4. Verify backend is running

---

## 📚 Documentation

- **SETUP_GUIDE.md** - Detailed setup instructions
- **README.md** - Complete feature documentation
- **IMPLEMENTATION_SUMMARY.md** - Architecture overview

---

## 🎓 What You Can Do Now

### User Features
- ✅ Register and login
- ✅ Browse 50+ sample questions
- ✅ Answer questions and get feedback
- ✅ Track your progress
- ✅ Get AI recommendations
- ✅ Bookmark important questions
- ✅ Filter by difficulty

### Admin Features (via Database)
- Add new exams
- Add subjects and topics
- Import questions (via PDF parser)
- View user statistics
- Analyze performance data

---

## 🚀 Next Steps

### Add More Questions
```bash
cd backend
python pdf_parser.py path/to/pdf output.csv
# Then import into database
```

### Customize Frontend
Edit `frontend/styles.css` for colors and fonts
Edit `frontend/app.js` for behavior
Update `frontend/index.html` for structure

### Adjust Recommendation Engine
Edit `backend/ml_recommender.py` to:
- Change accuracy threshold
- Adjust difficulty progression
- Customize learning paths

### Deploy to Production
See SETUP_GUIDE.md → Production Deployment section

---

## 💡 Tips

- **Reset Database**: Delete PostgreSQL data and reload schema.sql
- **Clear Browser Cache**: Ctrl+Shift+Delete in most browsers
- **Debug Mode**: Set `DEBUG=True` in .env for more error info
- **Watch Logs**: Keep terminal visible to see server messages

---

## 🎉 You're Ready!

Your Question Bank is now:
- ✅ **Running** locally
- ✅ **Populated** with sample data
- ✅ **Ready** to accept users
- ✅ **Equipped** with AI recommendations
- ✅ **Fully documented** for deployment

### Start Using: http://localhost:3000

---

**Questions?** Check:
1. SETUP_GUIDE.md
2. README.md
3. Browser console (F12)
4. Server logs (terminal)

**Happy Learning!** 📚

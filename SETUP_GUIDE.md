# Question Bank - Complete Setup Guide

This guide provides step-by-step instructions to get the Question Bank application running on your system.

## Quick Start (Using Docker) - Recommended

If you have Docker and Docker Compose installed, you can get the entire stack running with one command:

```bash
docker-compose up
```

Then visit:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

**That's it!** Docker handles all the setup automatically.

---

## Manual Setup

If you prefer to set up the project manually, follow these detailed steps.

### Prerequisites

Before starting, ensure you have installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/)

Verify installations:
```bash
python --version
psql --version
git --version
```

### Step 1: Clone or Extract Project

```bash
# If using git
git clone <repository-url>
cd question-bank

# Or if you downloaded the ZIP
unzip question-bank.zip
cd question-bank
```

### Step 2: Set Up PostgreSQL Database

**Windows/Mac/Linux:**

1. Open your PostgreSQL client (pgAdmin or command line)

2. Create the database:
```sql
CREATE DATABASE question_bank;
```

3. Load the schema:
```bash
psql -U postgres -d question_bank -f database/schema.sql
```

Verify the tables were created:
```bash
psql -U postgres -d question_bank -c "\dt"
```

You should see tables like `users`, `questions`, `exams`, etc.

**Connection String Format:**
```
postgresql://username:password@localhost:5432/question_bank
```

Example:
```
postgresql://postgres:yourpassword@localhost:5432/question_bank
```

### Step 3: Set Up Python Backend

```bash
# Navigate to backend directory
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

# Create .env file
cp .env.example .env

# Edit .env with your database credentials
# Open .env and update:
# DATABASE_URL=postgresql://username:password@localhost:5432/question_bank
```

**Edit `.backend/.env`:**
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/question_bank
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=0.0.0.0
PORT=8000
DEBUG=False
CORS_ORIGINS=*
```

### Step 4: Import Sample Data

```bash
# From backend directory with venv activated
python import_sample_data.py
```

Expected output:
```
============================================================
Question Bank Database - Sample Data Import
============================================================
✓ Database schema verified

Importing sample data...
✓ Imported 4 exams
✓ Imported 10 subjects
✓ Imported 25+ topics
✓ Imported 50+ sample questions with options
✓ Generated additional sample questions

============================================================
✓ Data import completed successfully!
============================================================
```

### Step 5: Run the Backend Server

```bash
# From backend directory with venv activated
python app.py

# OR using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Visit: http://localhost:8000/docs to see API documentation

### Step 6: Serve the Frontend

**Option A: Using Python's built-in server**
```bash
cd frontend
python -m http.server 3000
```

**Option B: Using Node.js (if installed)**
```bash
npm install -g http-server
cd frontend
http-server -p 3000
```

**Option C: Using VS Code Live Server**
- Install "Live Server" extension in VS Code
- Right-click `index.html` and select "Open with Live Server"

### Step 7: Access the Application

Open your browser and visit:
```
http://localhost:3000
```

You should see the Question Bank homepage. 

---

## Testing the Application

### Create a Test Account

1. Click "Get Started" or "Login" button
2. Click "Register here" to create new account
3. Fill in the form:
   - Username: `testuser`
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `testpassword123`
   - Target Exam: `SAT`
4. Click "Register"

### Practice Using the App

1. **Browse Questions**: Go to "Browse" tab
2. **Filter Questions**: Select Exam → Subject → Topic → Difficulty
3. **Answer Questions**: Click a question, select an option, click "Submit"
4. **View Progress**: Go to "Dashboard" to see your stats
5. **Bookmark Questions**: Click the bookmark button on question details

---

## Configuration Reference

### Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | Required | PostgreSQL connection string |
| `SECRET_KEY` | Required | JWT secret key (change in production!) |
| `ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Session timeout in minutes |
| `HOST` | 0.0.0.0 | Server host address |
| `PORT` | 8000 | Server port |
| `DEBUG` | False | Debug mode (never True in production!) |
| `CORS_ORIGINS` | * | Allowed origins for CORS |

### Frontend Configuration (app.js)

```javascript
const API_BASE_URL = 'http://localhost:8000/api';  // Backend URL
const STORAGE_KEY = 'qb_user';                      // Local storage key
const TOKEN_KEY = 'qb_token';                       // Token storage key
```

If running on different hosts, update `API_BASE_URL`:
- Local: `http://localhost:8000/api`
- Remote: `http://your-server.com/api`

---

## Troubleshooting

### Issue: "Database connection error"

**Solution:**
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Verify DATABASE_URL format
# Should be: postgresql://user:password@localhost:5432/question_bank

# Test connection
psql "postgresql://postgres:password@localhost:5432/question_bank"
```

### Issue: "CORS error - blocked by CORS policy"

**Solution:**
- The frontend is on different port than backend
- Check `API_BASE_URL` in `frontend/app.js`
- Verify `CORS_ORIGINS` in backend `.env`

```javascript
// frontend/app.js - Update if needed
const API_BASE_URL = 'http://localhost:8000/api';
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (get PID from above)
kill -9 <PID>

# Or use different port
uvicorn app:app --port 8001
```

### Issue: "Module not found error"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Questions not loading in frontend"

**Solution:**
1. Check browser console (F12 → Console tab)
2. Check Network tab to see if API calls are working
3. Verify backend is running: `curl http://localhost:8000/health`
4. Verify `API_BASE_URL` in app.js matches your backend URL

### Issue: "Login not working"

**Solution:**
```bash
# Verify sample data was imported
psql -U postgres -d question_bank -c "SELECT * FROM users LIMIT 1;"

# Check backend logs for errors
# Verify .env DATABASE_URL is correct
```

---

## Development Tips

### Enable Debug Mode

Edit `backend/.env`:
```
DEBUG=True
```

Then restart the backend. You'll see more detailed error messages.

### Database Inspection

```bash
# Connect to database
psql -U postgres -d question_bank

# List all tables
\dt

# View users
SELECT * FROM users;

# View questions
SELECT * FROM questions LIMIT 10;

# Count questions
SELECT COUNT(*) FROM questions;
```

### API Testing

Use **Postman** or **Insomnia** to test API endpoints:

1. Import API from http://localhost:8000/docs
2. Test endpoints:
   - Register: POST /api/auth/register
   - Login: POST /api/auth/login
   - Get Questions: GET /api/questions
   - Submit Answer: POST /api/progress/submit

### Browser DevTools

Press `F12` to open developer tools:
- **Console**: View JavaScript errors
- **Network**: See API calls and responses
- **Storage**: View localStorage (user data, tokens)
- **Elements**: Inspect HTML structure

---

## Production Deployment

### Before Deploying

1. **Change SECRET_KEY**
   ```bash
   # Generate a strong random key
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Set DEBUG=False**
   ```
   DEBUG=False
   ```

3. **Update CORS_ORIGINS**
   ```
   CORS_ORIGINS=https://yourdomain.com
   ```

4. **Use strong database passwords**

5. **Enable HTTPS** on your server

### Deploy with Docker

```bash
# Build image
docker build -t question-bank:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="your-production-db-url" \
  -e SECRET_KEY="your-secret-key" \
  question-bank:latest
```

### Deploy with Traditional Hosting

```bash
# On your server, clone repository
git clone <url>
cd question-bank/backend

# Create venv and install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Use gunicorn for production
pip install gunicorn
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Next Steps

1. **Explore the API Documentation**: Visit http://localhost:8000/docs
2. **Read the Main README**: See `README.md` for full feature documentation
3. **Customize**: Modify questions, exams, and topics in the database
4. **Scale**: Add more questions from the provided PDFs using `import_data.py`
5. **Deploy**: Follow production deployment instructions above

---

## Getting Help

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review **backend logs**: Check console output for error messages
3. Check **frontend console**: F12 → Console tab in browser
4. Check **database**: Use psql to verify data exists
5. Read **README.md** for more detailed documentation

---

## Quick Reference Commands

```bash
# Start everything with Docker
docker-compose up

# Backend only
cd backend && source venv/bin/activate && python app.py

# Frontend only
cd frontend && python -m http.server 3000

# Database inspection
psql -U postgres -d question_bank -c "SELECT * FROM questions LIMIT 5;"

# Import data
cd backend && python import_sample_data.py

# Run tests
pytest backend/tests/

# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

---

**Happy coding! 🚀**

For detailed feature documentation, see [README.md](README.md)

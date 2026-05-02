# Question Bank - Setup Instructions

## Project Structure

```
question-bank/
├── backend/                 # Python FastAPI Backend
│   ├── routes/             # API route handlers
│   │   ├── auth.py        # Authentication routes
│   │   ├── questions.py   # Question CRUD routes
│   │   ├── users.py       # User progress routes
│   │   ├── admin.py       # Admin panel routes
│   │   └── recommendations.py  # ML recommendations
│   ├── models.py           # SQLAlchemy ORM models
│   ├── database.py         # Database configuration
│   ├── main.py             # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env               # Environment variables
│   └── database/
│       └── schema.sql     # Database schema
├── frontend/               # HTML/CSS/JavaScript Frontend
│   ├── index.html         # Main HTML file
│   ├── css/
│   │   └── styles.css    # Stylesheets
│   ├── js/
│   │   ├── config.js     # Configuration
│   │   ├── api.js        # API wrapper
│   │   ├── app.js        # Main app logic
│   │   ├── auth.js       # Auth handlers
│   │   ├── dashboard.js  # Dashboard logic
│   │   ├── browse.js     # Browse questions
│   │   └── admin.js      # Admin panel
│   └── public/           # Static assets
└── README.md
```

## Backend Setup

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip or conda

### 2. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Setup

Create a PostgreSQL database:
```bash
createdb question_bank
```

Update `.env` with your database credentials:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/question_bank
```

Initialize the database:
```bash
# The tables will be created automatically on first run
python main.py
```

Or manually run the schema:
```bash
psql -U postgres -d question_bank -f database/schema.sql
```

### 4. Run Backend Server

```bash
python main.py
```

Server runs at `http://localhost:8000`
API Documentation available at `http://localhost:8000/docs`

## Frontend Setup

### 1. Update API Configuration

Edit `frontend/js/config.js` to match your backend URL:
```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api',
    // ... rest of config
};
```

### 2. Run Frontend

You can run the frontend using any web server. Simple options:

**Using Python:**
```bash
cd frontend
python -m http.server 3000
```

**Using Node.js (http-server):**
```bash
npm install -g http-server
cd frontend
http-server -p 3000
```

**Using PHP:**
```bash
cd frontend
php -S localhost:3000
```

Open `http://localhost:3000` in your browser.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Questions
- `GET /api/questions` - Get questions with filters
- `GET /api/questions/{id}` - Get single question
- `POST /api/questions/submit-answer` - Submit answer

### Bookmarks
- `POST /api/questions/bookmarks/{question_id}` - Bookmark question
- `GET /api/questions/bookmarks/list` - Get bookmarks
- `DELETE /api/questions/bookmarks/{question_id}` - Remove bookmark

### User Progress
- `GET /api/users/stats` - Get user statistics
- `GET /api/users/progress/{question_id}` - Get question progress
- `GET /api/users/history` - Get attempt history

### Recommendations
- `GET /api/recommendations/personalized` - Get recommendations
- `GET /api/recommendations/by-topic/{topic_id}` - Topic recommendations
- `POST /api/recommendations/retrain` - Retrain model

### Admin
- `POST /api/admin/exams` - Create exam
- `GET /api/admin/exams` - Get exams
- `POST /api/admin/subjects` - Create subject
- `GET /api/admin/subjects` - Get subjects
- `POST /api/admin/topics` - Create topic
- `GET /api/admin/topics` - Get topics
- `POST /api/admin/questions` - Create question
- `PUT /api/admin/questions/{id}` - Update question
- `DELETE /api/admin/questions/{id}` - Delete question
- `GET /api/admin/statistics` - Get statistics

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/question_bank
SECRET_KEY=your-secret-key-change-in-production
ADMIN_PASSWORD=admin123
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
ENVIRONMENT=development
PORT=8000
```

## Features

### User Features
- User authentication and profile management
- Browse and search questions by exam, subject, topic, difficulty
- Take quizzes and track progress
- Personalized recommendations based on weak topics
- Bookmark favorite questions
- Performance analytics and statistics

### Admin Features
- Create and manage exams, subjects, topics
- Add, update, delete questions
- Bulk import questions from PDFs
- View platform statistics
- Monitor user progress

### ML Features
- Personalized question recommendations
- Weak topic identification
- Difficulty progression
- Performance analytics

## Importing Questions from PDFs

1. Convert PDF files to CSV format with columns:
   - exam_id, subject_id, topic_id
   - question_text
   - option_a, option_b, option_c, option_d
   - correct_answer, explanation
   - difficulty_level

2. Use the admin panel or API to bulk import

## Troubleshooting

### CORS Errors
Update `CORS_ORIGINS` in `.env` to include your frontend URL

### Database Connection Failed
- Check PostgreSQL is running
- Verify `DATABASE_URL` in `.env`
- Ensure database and user exist

### API Not Responding
- Check backend server is running (`python main.py`)
- Verify `API_BASE_URL` in frontend config
- Check network connectivity

## Security Notes

- Change `SECRET_KEY` and `ADMIN_PASSWORD` in production
- Use environment variables for sensitive data
- Implement proper authentication on admin endpoints
- Use HTTPS in production
- Implement rate limiting
- Add input validation and sanitization

## Performance Optimization

- Add database indexes on frequently queried columns
- Implement caching for recommendations
- Use pagination for large result sets
- Compress frontend assets
- Implement lazy loading for questions

## Next Steps

1. Load sample questions from the provided PDFs
2. Create exams, subjects, and topics in admin panel
3. Test authentication and question browsing
4. Set up personalized recommendations
5. Configure email notifications
6. Implement real-time progress updates

# Question Bank - AI-Powered Exam Preparation Platform

A comprehensive ML-powered question bank application designed for exam preparation with personalized recommendations, progress tracking, and smart question filtering.

## Features

- **Vast Question Database**: 1000+ questions across multiple subjects and exams
- **AI-Powered Recommendations**: Machine learning algorithms suggest questions based on weak topics
- **User Authentication**: Secure login and registration with user profile management
- **Progress Tracking**: Track your learning journey with detailed statistics and analytics
- **Smart Filtering**: Filter questions by exam, subject, topic, and difficulty level
- **Bookmarking**: Save important questions for later review
- **Personalized Learning Path**: AI generates a customized learning roadmap based on performance
- **Multiple Question Types**: Support for multiple choice, true/false, and other question formats

## Tech Stack

### Frontend
- **HTML5**: Semantic markup for accessibility
- **CSS3**: Responsive design with modern styling
- **Vanilla JavaScript**: No dependencies, pure client-side logic
- **Features**: 
  - Responsive design (Mobile, Tablet, Desktop)
  - Real-time filtering and search
  - Modal-based authentication
  - Toast notifications

### Backend
- **Python 3.8+**: Modern Python for robust server
- **FastAPI**: High-performance async web framework
- **PostgreSQL**: Reliable relational database
- **SQLAlchemy**: ORM for database operations
- **JWT**: Secure token-based authentication
- **Bcrypt**: Password hashing and verification

### Machine Learning
- **Scikit-learn**: For collaborative filtering and content-based recommendations
- **Pandas & NumPy**: Data processing and analysis
- **Custom Algorithms**: 
  - Weak topic identification
  - Difficulty-based progression
  - Content similarity matching
  - Learning path generation

## Project Structure

```
question-bank/
├── frontend/
│   ├── index.html          # Main HTML structure
│   ├── styles.css          # CSS styling
│   └── app.js              # JavaScript application logic
├── backend/
│   ├── app.py              # FastAPI main application
│   ├── ml_recommender.py   # ML recommendation engine
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── database/
│   └── schema.sql          # PostgreSQL schema
├── data/
│   ├── sample_questions.csv # Sample question data
│   └── import_data.py       # Data import script
└── README.md               # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Node.js (optional, for serving frontend)
- Git

### Step 1: Set Up the Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE question_bank;

# Load schema
\c question_bank
\i database/schema.sql

# Verify tables were created
\dt
```

### Step 2: Set Up Backend

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

# Create .env file (copy from .env.example)
cp .env.example .env

# Update DATABASE_URL in .env with your PostgreSQL connection
# Format: postgresql://username:password@localhost:5432/question_bank
```

### Step 3: Import Sample Data

```bash
# Ensure you're in the backend directory with venv activated
python data/import_data.py

# This will populate the database with:
# - Exams (SAT, GRE, TOEFL, etc.)
# - Subjects (English, Math, etc.)
# - Topics (Grammar, Algebra, etc.)
# - 500+ sample questions
```

### Step 4: Run the Backend Server

```bash
# From backend directory with venv activated
python app.py

# OR using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Server will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Step 5: Serve the Frontend

```bash
# Option 1: Using Python's built-in server
cd frontend
python -m http.server 3000

# Option 2: Using Node.js http-server
npm install -g http-server
http-server frontend -p 3000

# Visit http://localhost:3000 in your browser
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Questions
- `GET /api/questions` - Get questions with filters
- `GET /api/questions/{id}` - Get question details

### Exams & Subjects
- `GET /api/exams` - Get all exams
- `GET /api/exams/{id}/subjects` - Get exam subjects
- `GET /api/subjects/{id}/topics` - Get subject topics

### User Progress
- `POST /api/progress/submit` - Submit answer
- `GET /api/progress/user` - Get user progress stats

### Recommendations
- `GET /api/recommendations` - Get personalized recommendations
- `GET /api/bookmarks` - Get bookmarked questions
- `POST /api/bookmarks/{id}` - Add bookmark
- `DELETE /api/bookmarks/{id}` - Remove bookmark

## Database Schema

### Tables Overview

1. **users** - User accounts and authentication
2. **exams** - Available exams (SAT, GRE, TOEFL, etc.)
3. **subjects** - Exam subjects (English, Math, etc.)
4. **topics** - Subject topics (Grammar, Algebra, etc.)
5. **questions** - Question content and metadata
6. **options** - Multiple choice options
7. **user_progress** - User answer history and performance
8. **bookmarks** - User bookmarked questions
9. **weak_topics** - Identified weak areas per user
10. **quiz_sessions** - Quiz attempt records

## Machine Learning Recommendations

### Algorithm Overview

The recommendation engine uses multiple strategies:

1. **Weak Topic Identification**
   - Calculates accuracy percentage for each topic
   - Identifies topics below 70% accuracy threshold
   - Prioritizes lowest-accuracy topics

2. **Personalized Question Suggestions**
   - Recommends unanswered questions from weak topics
   - Adjusts difficulty based on overall accuracy
   - Avoids previously attempted questions

3. **Content Similarity Matching**
   - Groups similar questions by topic and difficulty
   - Provides relevant practice questions

4. **Learning Path Generation**
   - Creates personalized study roadmap
   - Estimates study time needed
   - Focuses on weak areas first

### How It Works

```python
# Example: Get personalized recommendations
recommendations = engine.get_personalized_recommendations(user_id=1, limit=10)

# Identifies weak topics
weak_topics = engine.identify_weak_topics(user_id=1, threshold=70.0)

# Generates learning path
path = engine.get_user_learning_path(user_id=1)
```

## Usage Guide

### For Users

1. **Register/Login**: Create account and login to access personalized features
2. **Select Exam**: Choose target exam (SAT, GRE, TOEFL, etc.)
3. **Browse Questions**: Filter by subject, topic, and difficulty
4. **Practice**: Answer questions and get immediate feedback
5. **Track Progress**: View accuracy, weak topics, and learning suggestions
6. **Bookmark**: Save important questions for later review
7. **Get Recommendations**: Receive AI-suggested questions based on weak areas

### For Administrators

1. **Add Exams**: Create new exam types
2. **Add Questions**: Import bulk questions from CSV
3. **Manage Topics**: Organize questions into topics
4. **View Analytics**: Monitor user progress and platform usage

## Configuration

### Environment Variables (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5432/question_bank
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=0.0.0.0
PORT=8000
DEBUG=False
CORS_ORIGINS=*
```

### Frontend Configuration (app.js)

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
const STORAGE_KEY = 'qb_user';
const TOKEN_KEY = 'qb_token';
```

## Security Features

- **Password Security**: Bcrypt hashing with salt
- **JWT Authentication**: Secure token-based auth
- **CORS Protection**: Configurable cross-origin access
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy
- **Input Validation**: Pydantic models for request validation
- **Secure Cookies**: HTTP-only token storage recommendation

## Performance Optimization

1. **Database Indexing**: Strategic indexes on frequently queried columns
2. **Query Optimization**: Efficient filtering and pagination
3. **Caching**: Consider implementing Redis for session caching
4. **Lazy Loading**: Load questions on-demand
5. **Pagination**: Limit results returned per request

## Deployment

### Heroku Deployment

```bash
# Create Procfile
echo "web: gunicorn app:app" > backend/Procfile

# Push to Heroku
git push heroku main

# Set environment variables
heroku config:set DATABASE_URL=...
heroku config:set SECRET_KEY=...
```

### Docker Deployment

```bash
# Create Dockerfile for backend
docker build -t question-bank-api .
docker run -p 8000:8000 question-bank-api

# Create docker-compose.yml for full stack
docker-compose up
```

## Testing

```bash
# Run backend tests
pytest backend/tests/

# Test API endpoints
curl http://localhost:8000/health

# Test with Postman or Insomnia
# Import API collection from docs
```

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Verify DATABASE_URL in .env
# Format: postgresql://user:password@localhost:5432/question_bank
```

### API Not Responding
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check port 8000 is available
lsof -i :8000
```

### Frontend Not Loading Questions
1. Check browser console for CORS errors
2. Verify API_BASE_URL in app.js
3. Ensure backend is running
4. Check network tab in DevTools

## Future Enhancements

- [ ] Advanced ML models (Neural Networks for better recommendations)
- [ ] Real-time collaboration features
- [ ] Video tutorials and explanations
- [ ] Mobile app (React Native)
- [ ] Spaced repetition algorithm
- [ ] API rate limiting and analytics
- [ ] Admin dashboard for content management
- [ ] Question difficulty calibration
- [ ] Social features (groups, leaderboards)
- [ ] Integration with popular learning platforms

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@questionbank.dev
- Documentation: https://docs.questionbank.dev

## Authors

- AI Development Team

## Acknowledgments

- FastAPI documentation and community
- PostgreSQL documentation
- Scikit-learn team for ML algorithms
- All contributors and users

---

**Happy Learning! 📚**

Start preparing for your exams with our AI-powered question bank today!
